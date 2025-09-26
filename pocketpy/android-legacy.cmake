# Miku's Custom CMake Toolchain File for Legacy Android NDK
set(CMAKE_SYSTEM_NAME Android)
set(CMAKE_SYSTEM_VERSION 14) # API level 14 for Android 4.0

# Specify the new standalone toolchain
set(TOOLCHAIN_PATH /tmp/my-android-toolchain)
set(CMAKE_SYSROOT ${TOOLCHAIN_PATH}/sysroot)

# Specify the cross-compilers
set(CMAKE_C_COMPILER ${TOOLCHAIN_PATH}/bin/arm-linux-androideabi-gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PATH}/bin/arm-linux-androideabi-g++)

# Set compiler flags for armv6
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -march=armv6 -mfloat-abi=softfp -mfpu=vfp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=armv6 -mfloat-abi=softfp -mfpu=vfp")

# Where to find headers and libraries
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
