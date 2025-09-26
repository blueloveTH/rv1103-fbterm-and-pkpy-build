SET(CMAKE_SYSTEM_NAME Linux)
SET(CMAKE_SYSTEM_PROCESSOR arm)

# 交叉编译器前缀
SET(TOOLCHAIN_PREFIX /home/miku/luckfox-pico/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf)

SET(CMAKE_C_COMPILER   ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-gcc)
SET(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-g++)
SET(CMAKE_AR           ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-ar)
SET(CMAKE_LINKER       ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-ld)
SET(CMAKE_NM           ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-nm)
SET(CMAKE_OBJCOPY      ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-objcopy)
SET(CMAKE_OBJDUMP      ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-objdump)
SET(CMAKE_RANLIB       ${TOOLCHAIN_PREFIX}/bin/arm-rockchip830-linux-uclibcgnueabihf-ranlib)

