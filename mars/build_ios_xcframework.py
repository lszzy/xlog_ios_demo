#!/usr/bin/env python3
import os
import sys
import glob

from mars_utils import *

# release/ios/2024-t2.1

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]

BUILD_OUT_PATH = 'cmake_build/iOS'
INSTALL_PATH = BUILD_OUT_PATH + '/iOS.out'
INSTALL_PATH_SIMULATOR_X86_64 = INSTALL_PATH + '/simulator_x86_64'
INSTALL_PATH_SIMULATOR_ARM64 = INSTALL_PATH + '/simulator_arm64'
INSTALL_PATH_OS_ARM64 = INSTALL_PATH + '/os_arm64'

IOS_BUILD_SIMULATOR_X86_64_CMD = 'cmake ../.. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=../../ios.xcframework.toolchain.cmake -DPLATFORM=SIMULATORARM64 -DENABLE_ARC=0 -DENABLE_BITCODE=0 -DENABLE_VISIBILITY=1 && make -j8 && make install'
IOS_BUILD_SIMULATOR_ARM64_CMD = 'cmake ../.. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=../../ios.xcframework.toolchain.cmake -DPLATFORM=SIMULATOR64 -DENABLE_ARC=0 -DENABLE_BITCODE=0 -DENABLE_VISIBILITY=1 && make -j8 && make install'
IOS_BUILD_OS_ARM64_CMD = 'cmake ../.. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=../../ios.xcframework.toolchain.cmake -DPLATFORM=OS -DENABLE_ARC=0 -DENABLE_BITCODE=0 -DENABLE_VISIBILITY=1 && make -j8 && make install'

def build_ios_xlog_simulator_x86_64(tag=''):
    gen_mars_revision_file('comm', tag)
    
    clean(BUILD_OUT_PATH)
    os.chdir(BUILD_OUT_PATH)
    
    ret = os.system(IOS_BUILD_SIMULATOR_X86_64_CMD)
    os.chdir(SCRIPT_PATH)
    if ret != 0:
        print('!!!!!!!!!!!build simulator fail!!!!!!!!!!!!!!!')
        return False

    libtool_simulator_dst_lib = INSTALL_PATH + '/simulator'
    libtool_src_libs = [INSTALL_PATH + '/libcomm.a',
                        INSTALL_PATH + '/libmars-boost.a',
                        INSTALL_PATH + '/libxlog.a',
                        BUILD_OUT_PATH + '/zstd/libzstd.a']
    if not libtool_libs(libtool_src_libs, libtool_simulator_dst_lib):
        return False

    lipo_src_libs = []
    lipo_src_libs.append(libtool_simulator_dst_lib)
    lipo_dst_lib = INSTALL_PATH + '/mars'

    if not lipo_libs(lipo_src_libs, lipo_dst_lib):
        return False

    dst_framework_path = INSTALL_PATH_SIMULATOR_X86_64 + '/mars.framework'
    make_static_framework(lipo_dst_lib, dst_framework_path, XLOG_COPY_HEADER_FILES, '../')

    print('==================Output========================')
    print(dst_framework_path)

def build_ios_xlog_simulator_arm64(tag=''):
    gen_mars_revision_file('comm', tag)
    
    clean(BUILD_OUT_PATH)
    os.chdir(BUILD_OUT_PATH)
    
    ret = os.system(IOS_BUILD_SIMULATOR_ARM64_CMD)
    os.chdir(SCRIPT_PATH)
    if ret != 0:
        print('!!!!!!!!!!!build simulator fail!!!!!!!!!!!!!!!')
        return False

    libtool_simulator_dst_lib = INSTALL_PATH + '/simulator'
    libtool_src_libs = [INSTALL_PATH + '/libcomm.a',
                        INSTALL_PATH + '/libmars-boost.a',
                        INSTALL_PATH + '/libxlog.a',
                        BUILD_OUT_PATH + '/zstd/libzstd.a']
    if not libtool_libs(libtool_src_libs, libtool_simulator_dst_lib):
        return False

    lipo_src_libs = []
    lipo_src_libs.append(libtool_simulator_dst_lib)
    lipo_dst_lib = INSTALL_PATH + '/mars'

    if not lipo_libs(lipo_src_libs, lipo_dst_lib):
        return False

    dst_framework_path = INSTALL_PATH_SIMULATOR_ARM64 + '/mars.framework'
    make_static_framework(lipo_dst_lib, dst_framework_path, XLOG_COPY_HEADER_FILES, '../')

    print('==================Output========================')
    print(dst_framework_path)

def build_ios_xlog_os_arm64(tag=''):
    gen_mars_revision_file('comm', tag)
    
    clean(BUILD_OUT_PATH)
    os.chdir(BUILD_OUT_PATH)
    
    ret = os.system(IOS_BUILD_OS_ARM64_CMD)
    os.chdir(SCRIPT_PATH)
    if ret != 0:
        print('!!!!!!!!!!!build os fail!!!!!!!!!!!!!!!')
        return False

    libtool_os_dst_lib = INSTALL_PATH + '/os'
    libtool_src_libs = [INSTALL_PATH + '/libcomm.a',
                        INSTALL_PATH + '/libmars-boost.a',
                        INSTALL_PATH + '/libxlog.a',
                        BUILD_OUT_PATH + '/zstd/libzstd.a']
    if not libtool_libs(libtool_src_libs, libtool_os_dst_lib):
        return False

    lipo_src_libs = []
    lipo_src_libs.append(libtool_os_dst_lib)
    lipo_dst_lib = INSTALL_PATH + '/mars'

    if not lipo_libs(lipo_src_libs, lipo_dst_lib):
        return False

    dst_framework_path = INSTALL_PATH_OS_ARM64 + '/mars.framework'
    make_static_framework(lipo_dst_lib, dst_framework_path, XLOG_COPY_HEADER_FILES, '../')

    print('==================Output========================')
    print(dst_framework_path)

def build_ios_xlog_xcframework():
    os.chdir(INSTALL_PATH)
    os.system('mkdir simulator_all')
    os.system('lipo -create simulator_arm64/mars.framework/mars simulator_x86_64/mars.framework/mars -output simulator_all/mars')
    os.system('cp -r simulator_arm64/mars.framework simulator_all/mars.framework')
    os.system('rm simulator_all/mars.framework/mars')
    os.system('mv simulator_all/mars simulator_all/mars.framework/mars')

    dst_xcframework_path = INSTALL_PATH + '/mars.xcframework'
    os.system('xcodebuild -create-xcframework -framework simulator_all/mars.framework -framework os_arm64/mars.framework -output mars.xcframework')
    print('==================Output========================')
    print(dst_xcframework_path)

def main():
    build_ios_xlog_simulator_x86_64()
    build_ios_xlog_simulator_arm64()
    build_ios_xlog_os_arm64()
    build_ios_xlog_xcframework()

if __name__ == '__main__':
    main()
