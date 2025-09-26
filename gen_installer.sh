#!/bin/bash

# =================================================================
# Luckfox Pico 项目部署包生成脚本 (v3 - 包含权限自动处理)
#
# 该脚本会执行以下操作:
# 1. 创建一个临时的根文件系统目录。
# 2. 将 'dep' 和 'output' 目录的内容合并进去。
# 3. 在打包前，为所有可执行文件和脚本智能地设置 +x 权限。
# 4. 将临时目录打包成一个保留权限的 'update.tar' 文件。
# 5. 生成一个在目标板上运行的、带权限校验的智能安装脚本 'install.sh'。
# 6. 将最终产物放置在 'install/' 目录。
# =================================================================

set -eu

# --- 变量定义 ---
BUILD_DIR=$(pwd)
OUTPUT_DIR="${BUILD_DIR}/output"
DEP_DIR="${BUILD_DIR}/dep"
PACKAGE_DIR="${BUILD_DIR}/install"
PACKAGE_ROOT="${BUILD_DIR}/package_root" # 用于合并文件的临时目录
TAR_FILE="${PACKAGE_DIR}/update.tar"
INSTALL_SCRIPT="${PACKAGE_DIR}/install.sh"

# --- 检查源目录是否存在 ---
if [ ! -d "${OUTPUT_DIR}" ]; then
    echo "错误: 'output' 目录不存在。请先运行编译脚本。"
    exit 1
fi
if [ ! -d "${DEP_DIR}" ]; then
    echo "错误: 'dep' 目录不存在。"
    exit 1
fi


# --- 1. 清理并创建打包目录 ---
echo "====== 1. 正在准备打包环境... ======"
rm -rf "${PACKAGE_ROOT}" "${PACKAGE_DIR}"
mkdir -p "${PACKAGE_ROOT}"
mkdir -p "${PACKAGE_DIR}"
echo "临时目录 '${PACKAGE_ROOT}' 和输出目录 '${PACKAGE_DIR}' 已准备就绪。"
echo ""


# --- 2. 合并文件 ---
echo "====== 2. 正在合并 'dep' 和 'output' 目录... ======"
rsync -a "${DEP_DIR}/" "${PACKAGE_ROOT}/"
rsync -a "${OUTPUT_DIR}/" "${PACKAGE_ROOT}/"
echo "文件合并完成。"
echo ""


# --- 3. 在打包前，预设文件权限 ---
echo "====== 3. 正在预设可执行文件权限... ======"
# 为我们编译的主要程序赋予可执行权限
chmod +x "${PACKAGE_ROOT}/usr/bin/fbterm"
chmod +x "${PACKAGE_ROOT}/usr/bin/pocketpy"
chmod +x "${PACKAGE_ROOT}/usr/bin/fc-"*

# 递归查找所有 .sh 脚本并赋予可执行权限
find "${PACKAGE_ROOT}" -type f -name "*.sh" -exec chmod +x {} \;
echo "权限预设完成。"
echo ""


# --- 4. 打包成 Tar 文件 ---
echo "====== 4. 正在将合并后的文件打包成 ${TAR_FILE}... ======"
# 使用 -p 参数来确保文件权限被完整保留
tar -cpf "${TAR_FILE}" -C "${PACKAGE_ROOT}" .
echo "打包完成。"
echo ""


# --- 5. 清理临时目录 ---
echo "====== 5. 正在清理临时文件... ======"
rm -rf "${PACKAGE_ROOT}"
echo "清理完成。"
echo ""


# --- 6. 生成一键安装脚本 (install.sh) ---
echo "====== 6. 正在生成目标板安装脚本 (install.sh)... ======"
cat << 'EOF' > "${INSTALL_SCRIPT}"
#!/bin/sh
# =================================================
# System Update & Setup Script (v2)
# To be executed on the target device.
# =================================================
set -e

# --- Configuration ---
SWAPFILE_PATH="/root/swapfile"
SWAPFILE_SIZE_MB=128
DISK_IMG_PATH="/root/mass.img"
DISK_IMG_SIZE_MB=64

echo "====== Starting System Update & Setup ======"

if [ ! -f "update.tar" ]; then
    echo "Error: update.tar not found! Please place this script in the same directory as update.tar."
    exit 1
fi

# 1. Special handling for specified /etc subdirectories
echo "--> Preparing /etc directories..."
rm -rf /etc/init.d
rm -rf /etc/profile.d
echo "Old /etc directories removed."

# 2. Extract the archive to the root filesystem
echo "--> Extracting update.tar to root filesystem (preserving permissions)..."
# 使用 -p 参数来确保从压缩包中恢复权限
tar -xpf update.tar -C /
echo "Extraction complete."

# 3. Failsafe: Ensure all shell scripts are executable
echo "--> Verifying executable permissions for shell scripts..."
# 遍历关键目录，为所有 .sh 文件再次确保 +x 权限
find /etc /oem /root /usr -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
echo "Permissions verified."

# 4. Check for and create swapfile if it doesn't exist
echo "--> Checking for swapfile at ${SWAPFILE_PATH}..."
if [ ! -f "${SWAPFILE_PATH}" ]; then
    echo "Swapfile not found. Creating a ${SWAPFILE_SIZE_MB}MB swapfile..."
    dd if=/dev/zero of="${SWAPFILE_PATH}" bs=1M count=${SWAPFILE_SIZE_MB}
    chmod 600 "${SWAPFILE_PATH}"
    mkswap "${SWAPFILE_PATH}"
    echo "Swapfile created successfully."
    echo "NOTE: To activate it on boot, add '/root/swapfile none swap sw 0 0' to /etc/fstab."
else
    echo "Swapfile already exists. Skipping creation."
fi

# 5. Check for and create mass storage image if it doesn't exist
echo "--> Checking for disk image at ${DISK_IMG_PATH}..."
if [ ! -f "${DISK_IMG_PATH}" ]; then
    echo "Disk image not found. Creating a ${DISK_IMG_SIZE_MB}MB image..."
    dd if=/dev/zero of="${DISK_IMG_PATH}" bs=1M count=${DISK_IMG_SIZE_MB}
    mkfs.fat "${DISK_IMG_PATH}"
    echo "Disk image created and formatted as FAT successfully."
else
    echo "Disk image already exists. Skipping creation."
fi

# 6. Cleanup
echo "--> Cleaning up installation files..."
rm update.tar
echo "Update process finished! This script will now self-destruct."
rm -- "$0"

echo "====== System Update & Setup Complete! A reboot is recommended. ======"
EOF

chmod +x "${INSTALL_SCRIPT}"
echo "安装脚本 'install.sh' 生成完毕。"
echo ""


# --- 7. 打印最终的部署说明 ---
echo "================================================================="
echo "✅ 部署包已成功创建！"
echo ""
echo "下一步，请按照以下步骤在 Luckfox Pico 开发板上进行部署："
echo ""
echo "1. 将 'install' 目录下的所有文件 (update.tar 和 install.sh)，通过 scp 或其他方式，上传到板子的某个临时目录（例如 /tmp）:"
echo ""
echo "   示例 scp 命令 (请将 <board_ip> 替换为板子的实际IP):"
echo "   scp install/* root@<board_ip>:/tmp/"
echo ""
echo "2. SSH 登录到你的开发板，然后执行以下命令："
echo "   cd /tmp"
echo "   ./install.sh"
echo ""
echo "3. 脚本会自动完成所有部署工作并自我清理。完成后，建议重启开发板。"
echo "================================================================="
