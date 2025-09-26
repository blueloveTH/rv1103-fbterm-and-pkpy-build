#!/bin/bash

# =================================================================
# Fbterm 全自动交叉编译脚本 (v9 - Final)
#
# 该脚本将在一台全新的 Debian/Ubuntu 主机上自动完成所有操作：
# 1. 安装所有必需的系统软件包。
# 2. 自动下载并设置交叉编译工具链。
# 3. 自动检查并按需升级 Autoconf 版本。
# 4. 按顺序编译所有依赖库和 fbterm 主程序。
#
# 使用方法:
# 1. 将此脚本与所有源码压缩包放在同一个目录下。
# 2. 给予脚本执行权限: chmod +x build_all.sh
# 3. 运行脚本: ./build_all.sh
# =================================================================

set -eu

# =================================================================
# 第一部分：安装编译主机所需的所有依赖包
# =================================================================
echo "====== 1.1 正在安装编译主机所有依赖包 (可能需要您输入sudo密码) ======"
sudo apt-get update
# 合并了厂商推荐列表和我们之前确定的列表
sudo apt-get install -y \
    git ssh make gcc gcc-multilib g++-multilib module-assistant expect g++ \
    gawk texinfo libssl-dev bison flex fakeroot cmake unzip gperf autoconf \
    device-tree-compiler libncurses5-dev pkg-config bc python-is-python3 \
    openssl openssh-server openssh-client vim file cpio rsync \
    build-essential automake libtool uuid-dev wget xz-utils
echo "====== 主机依赖包安装完毕. ======"
echo ""


# =================================================================
# 第二部分：自动下载并设置交叉编译工具链
# =================================================================
BUILD_DIR=$(pwd)
TOOLCHAIN_PARENT_DIR="${BUILD_DIR}/luckfox_toolchain"
TOOLCHAIN_DIR="${TOOLCHAIN_PARENT_DIR}/luckfox-pico/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf"
TOOLCHAIN_BIN_PATH="${TOOLCHAIN_DIR}/bin"

echo "====== 2.1 检查交叉编译工具链... ======"
if [ ! -d "${TOOLCHAIN_DIR}" ]; then
    echo "工具链不存在，正在从 Gitee 克隆..."
    # 使用 --depth 1 进行浅克隆，大大加快下载速度
    git clone --depth 1 https://gitee.com/LuckfoxTECH/luckfox-pico.git "${TOOLCHAIN_PARENT_DIR}"
    echo "工具链克隆完成。"
else
    echo "工具链已存在于: ${TOOLCHAIN_PARENT_DIR}"
fi
echo ""


# =================================================================
# 第三部分：自动检查并升级 Autoconf
# =================================================================
echo "====== 3.1 检查 Autoconf 版本... ======"
AUTOCONF_REQUIRED_VERSION="2.71"
INSTALLED_AUTOCONF_VERSION=$(autoconf --version | head -n 1 | awk '{print $NF}' || echo "0")
LOWEST_VERSION=$(printf '%s\n' "$AUTOCONF_REQUIRED_VERSION" "$INSTALLED_AUTOCONF_VERSION" | sort -V | head -n1)

if [ "$LOWEST_VERSION" != "$AUTOCONF_REQUIRED_VERSION" ]; then
    echo "警告: 当前 Autoconf 版本 ($INSTALLED_AUTOCONF_VERSION) 过低, 需要 >= $AUTOCONF_REQUIRED_VERSION."
    echo "====== 正在自动下载并编译新版 Autoconf 2.72 ======"
    
    TEMP_BUILD_DIR=${BUILD_DIR}/build_temp
    mkdir -p "$TEMP_BUILD_DIR"
    cd "$TEMP_BUILD_DIR"

    wget -q --show-progress https://ftp.wayne.edu/gnu/autoconf/autoconf-2.72.tar.gz
    tar -xzf autoconf-2.72.tar.gz
    cd autoconf-2.72
    
    echo "正在配置 Autoconf..."
    ./configure --prefix=/usr/local
    echo "正在编译 Autoconf..."
    make -j$(nproc)
    
    echo "正在使用 sudo 安装 Autoconf 到 /usr/local/bin (需要您的密码)..."
    sudo make install
    
    cd ../..
    rm -rf "$TEMP_BUILD_DIR"

    hash -r
    echo "====== Autoconf 升级完成. ======"
else
    echo "当前 Autoconf 版本 ($INSTALLED_AUTOCONF_VERSION) 满足要求, 无需升级."
fi
echo "确认最终 Autoconf 版本:"
which autoconf
autoconf --version
echo ""


# --- 核心编译环境变量设置 ---
TOOLCHAIN_PREFIX="arm-rockchip830-linux-uclibcgnueabihf-"
TARGET_HOST="arm-linux"
INSTALL_DIR="${BUILD_DIR}/staging"

export PATH="${TOOLCHAIN_BIN_PATH}:${PATH}"
export CC="${TOOLCHAIN_PREFIX}gcc"
export CXX="${TOOLCHAIN_PREFIX}g++"
export LD="${TOOLCHAIN_PREFIX}ld"
export AR="${TOOLCHAIN_PREFIX}ar"
export AS="${TOOLCHAIN_PREFIX}as"
export NM="${TOOLCHAIN_PREFIX}nm"
export RANLIB="${TOOLCHAIN_PREFIX}ranlib"
export STRIP="${TOOLCHAIN_PREFIX}strip"
export PKG_CONFIG_PATH="${INSTALL_DIR}/lib/pkgconfig"
export CPPFLAGS="-I${INSTALL_DIR}/include"
export CXXFLAGS="-g -O2"
export LDFLAGS="-L${INSTALL_DIR}/lib"
export LIBS=""


# =================================================================
# 第四部分：按顺序编译所有依赖和主程序
# =================================================================
rm -rf "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}"

echo "================================================================="
echo "交叉编译环境设置完毕:"
echo "  - 安装目录: ${INSTALL_DIR}"
echo "  - C 编译器: $(which ${CC})"
echo "================================================================="

# --- 编译 zlib ---
echo ""
echo "======== 4.1 正在编译 zlib-1.3.1 ========"
cd "${BUILD_DIR}/zlib-1.3.1"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --static
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== zlib 编译完成. ========"

# --- 编译 expat ---
echo ""
echo "======== 4.2 正在编译 expat-2.7.1 ========"
cd "${BUILD_DIR}/expat-2.7.1"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --enable-static --disable-shared --without-docbook
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== expat 编译完成. ========"

# --- 编译 libiconv ---
echo ""
echo "======== 4.3 正在编译 libiconv-1.7 ========"
cd "${BUILD_DIR}/libiconv-1.7"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --enable-static --disable-shared
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== libiconv 编译完成. ========"

# --- 编译 freetype ---
echo ""
echo "======== 4.4 正在编译 freetype-2.10.0 ========"
cd "${BUILD_DIR}/freetype-2.10.0"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --with-zlib=yes --enable-static --disable-shared
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== freetype 编译完成. ========"

# --- 编译 fontconfig ---
echo ""
echo "======== 4.5 正在编译 fontconfig-2.16.0 ========"
cd "${BUILD_DIR}/fontconfig-2.16.0"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --enable-static --disable-shared --disable-docs \
            --sysconfdir=${INSTALL_DIR}/etc --localstatedir=${INSTALL_DIR}/var
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== fontconfig 编译完成. ========"

# --- 编译 fbterm ---
echo ""
echo "======== 4.6 正在编译 fbterm-1.7 ========"
cd "${BUILD_DIR}/fbterm-1.7"

ORIGINAL_CXXFLAGS="${CXXFLAGS}"
ORIGINAL_LIBS="${LIBS}"
export CXXFLAGS="${CXXFLAGS} -Wno-narrowing -fpermissive"
export LIBS="-liconv -lexpat -lz"
echo "为 fbterm 应用特殊编译参数: CXXFLAGS='${CXXFLAGS}' LIBS='${LIBS}'"

make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}"
make -j$(nproc)

export CXXFLAGS="${ORIGINAL_CXXFLAGS}"
export LIBS="${ORIGINAL_LIBS}"

echo "fbterm 可执行文件位于: ${BUILD_DIR}/fbterm-1.7/fbterm"
cd "${BUILD_DIR}"
echo "======== fbterm 编译完成. ========"


echo ""
echo "================================================================="
echo "所有项目编译成功!"
echo "所有依赖库已安装到: ${INSTALL_DIR}"
echo "fbterm 可执行文件为: ${BUILD_DIR}/fbterm-1.7/fbterm"
echo "================================================================="
