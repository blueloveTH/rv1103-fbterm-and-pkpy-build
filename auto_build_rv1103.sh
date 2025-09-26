#!/bin/bash

# =================================================================
# Fbterm 及其依赖项交叉编译脚本 (v8 - 修正 libiconv 静态链接)
# =================================================================

set -eu

# ... (Part 1: Host dependency installation and Autoconf upgrade remain the same) ...
echo "====== 1.1 正在安装编译主机基础依赖包 (可能需要您输入sudo密码) ======"
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    autoconf \
    automake \
    libtool \
    pkg-config \
    uuid-dev \
    gperf \
    wget \
    xz-utils \
    python3
echo "====== 主机基础依赖包安装完毕. ======"
echo ""

echo "====== 1.2 检查 Autoconf 版本... ======"
AUTOCONF_REQUIRED_VERSION="2.71"
INSTALLED_AUTOCONF_VERSION=$(autoconf --version | head -n 1 | awk '{print $NF}' || echo "0")
LOWEST_VERSION=$(printf '%s\n' "$AUTOCONF_REQUIRED_VERSION" "$INSTALLED_AUTOCONF_VERSION" | sort -V | head -n1)

if [ "$LOWEST_VERSION" != "$AUTOCONF_REQUIRED_VERSION" ]; then
    echo "警告: 当前 Autoconf 版本 ($INSTALLED_AUTOCONF_VERSION) 过低, 需要 >= $AUTOCONF_REQUIRED_VERSION."
    echo "====== 正在自动下载并编译新版 Autoconf 2.72 ======"
    TEMP_BUILD_DIR=$(pwd)/build_temp
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


# --- Configuration Variables ---
TOOLCHAIN_BIN_PATH="/home/miku/luckfox-pico/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf/bin"
TOOLCHAIN_PREFIX="arm-rockchip830-linux-uclibcgnueabihf-"
TARGET_HOST="arm-linux"
BUILD_DIR=$(pwd)
INSTALL_DIR="${BUILD_DIR}/staging"

# --- Environment Variables ---
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

# --- Build Process ---
rm -rf "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}"

echo "================================================================="
echo "交叉编译环境设置完毕:"
echo "  - 安装目录: ${INSTALL_DIR}"
echo "  - C 编译器: $(which ${CC})"
echo "================================================================="

# ... (zlib, expat, libiconv, freetype, fontconfig builds remain the same) ...
# --- Build zlib ---
echo ""
echo "======== 2. 正在编译 zlib-1.3.1 ========"
cd "${BUILD_DIR}/zlib-1.3.1"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --static
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== zlib 编译完成. ========"
# --- Build expat ---
echo ""
echo "======== 3. 正在编译 expat-2.7.1 ========"
cd "${BUILD_DIR}/expat-2.7.1"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --enable-static --disable-shared --without-docbook
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== expat 编译完成. ========"
# --- Build libiconv ---
echo ""
echo "======== 4. 正在编译 libiconv-1.7 ========"
cd "${BUILD_DIR}/libiconv-1.7"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --enable-static --disable-shared
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== libiconv 编译完成. ========"
# --- Build freetype ---
echo ""
echo "======== 5. 正在编译 freetype-2.10.0 ========"
cd "${BUILD_DIR}/freetype-2.10.0"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --with-zlib=yes --enable-static --disable-shared
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== freetype 编译完成. ========"
# --- Build fontconfig ---
echo ""
echo "======== 6. 正在编译 fontconfig-2.16.0 ========"
cd "${BUILD_DIR}/fontconfig-2.16.0"
make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}" --enable-static --disable-shared --disable-docs \
            --sysconfdir=${INSTALL_DIR}/etc --localstatedir=${INSTALL_DIR}/var
make -j$(nproc)
make install
cd "${BUILD_DIR}"
echo "======== fontconfig 编译完成. ========"

# --- Build fbterm ---
echo ""
echo "======== 7. 正在编译 fbterm-1.7 ========"
cd "${BUILD_DIR}/fbterm-1.7"

# --- MODIFICATION: Manually add all static link dependencies for fbterm ---
ORIGINAL_CXXFLAGS="${CXXFLAGS}"
ORIGINAL_LIBS="${LIBS:-}"

export CXXFLAGS="${CXXFLAGS} -Wno-narrowing -fpermissive"
# Add ALL required libraries: iconv, expat, and zlib
export LIBS="-liconv -lexpat -lz"
echo "为 fbterm 应用特殊编译参数: CXXFLAGS='${CXXFLAGS}' LIBS='${LIBS}'"
# --------------------------------------------------------------------------

make clean &> /dev/null || true
./configure --prefix="${INSTALL_DIR}" --host="${TARGET_HOST}"
make -j$(nproc)

# --- Restore original environment variables ---
export CXXFLAGS="${ORIGINAL_CXXFLAGS}"
export LIBS="${ORIGINAL_LIBS}"
# -----------------------------------------------

echo "fbterm 可执行文件位于: ${BUILD_DIR}/fbterm-1.7/fbterm"
cd "${BUILD_DIR}"
echo "======== fbterm 编译完成. ========"


echo ""
echo "================================================================="
echo "所有项目编译成功!"
echo "所有依赖库已安装到: ${INSTALL_DIR}"
echo "fbterm 可执行文件为: ${BUILD_DIR}/fbterm-1.7/fbterm"
echo "================================================================="
