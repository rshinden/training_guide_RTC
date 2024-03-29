cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(Calc NONE)

set(CMAKE_ALLOW_LOOSE_LOOP_CONSTRUCTS true)
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake_modules")

set(LINUX_PACKAGE_GENERATOR "DEB")
#set(LINUX_PACKAGE_GENERATOR "RPM")


# component settings
set(RTC_NAME "${PROJECT_NAME}")
set(RTC_VERSION "1.0.0")
set(RTC_VERSION_MAJOR "1")
set(RTC_VERSION_MINOR "0")
set(RTC_VERSION_PATCH "0")
set(RTC_LANG "python")
set(RTC_DESCRIPTION "ModuleDescription")
set(RTC_VENDOR "Shinden")
set(RTC_MAINTAINER "author@example.com")

string(TOLOWER ${RTC_NAME} PACKAGE_NAME)
set(PACKAGE_VERSION "${RTC_VERSION_MAJOR}.${RTC_VERSION_MINOR}.${RTC_VERSION_PATCH}")

set(IDL_FILES ""
)

set(EXEC_FILES ""
               Calc.py
)

set(OTHER_SRCS CMakeLists.txt
               RTC.xml Calc.conf rtc.conf)


# check OpenRTM installed
find_package(OpenRTMPython REQUIRED)

# check doxygen installed
find_package(Doxygen)
if(DOXYGEN_FOUND STREQUAL "NO")
    message(FATAL_ERROR "Doxygen not found.")
endif()

# check python installed
find_package(PythonInterp)
find_package(PythonLibs)


if(WIN32)
    # add command path
    set($ENV{PATH} $ENV{PATH} "${OPENRTM_DIR}/bin")
    # set install path prefix
    set(CMAKE_INSTALL_PREFIX "${OPENRTM_DIR}")
    set(INSTALL_PREFIX "components/${RTC_LANG}/${PACKAGE_NAME}${PACKAGE_VERSION}")
else()
    # add command path
    set($ENV{PATH} $ENV{PATH} "${OPENRTM_DIR}/bin")
    # set install path prefix
    set(CMAKE_INSTALL_PREFIX "${OPENRTM_DIR}")
    set(OPENRTM_SHARE_PREFIX "share/openrtm-${OPENRTM_VERSION_MAJOR}.${OPENRTM_VERSION_MINOR}")
    set(INSTALL_PREFIX "${OPENRTM_SHARE_PREFIX}/components/${RTC_LANG}/${PACKAGE_NAME}${PACKAGE_VERSION}")
endif()


# add uninstall target
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/uninstall_target.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/uninstall_target.cmake"
    IMMEDIATE @ONLY)
add_custom_target(uninstall COMMAND 
    ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)


# add build target
add_custom_target(build ALL)

add_custom_command(TARGET build PRE_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory bin)

foreach(idl ${IDL_FILES})
    add_custom_command(TARGET build PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -E echo "IDL Compiling \"${idl}\""
        COMMAND ${OPENRTM_IDLC} ${OPENRTM_IDLFLAGS} -Cbin "${PROJECT_SOURCE_DIR}/${idl}")
endforeach()

install(PROGRAMS ${EXEC_FILES} DESTINATION "${INSTALL_PREFIX}"
        COMPONENT "applications")

install(FILES RTC.xml DESTINATION "${INSTALL_PREFIX}"
        COMPONENT "applications")

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin/ DESTINATION "${INSTALL_PREFIX}"
        COMPONENT "applications"
        PATTERN "bin/*")


# target settings for document
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/doc/doxyfile.in"
               "${CMAKE_CURRENT_BINARY_DIR}/doc/doxyfile")

add_custom_target(doxygen COMMAND
                  ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/doxyfile)

set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES doc)

get_target_property(DOC_TARGET doc TYPE)
if(NOT DOC_TARGET)
    add_custom_target(doc)
endif()
add_dependencies(doc doxygen)

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/doc DESTINATION "${INSTALL_PREFIX}"
        COMPONENT "documents")


# install source files
install(FILES ${IDL_FILES} ${EXEC_FILES} ${OTHER_SRCS}
        DESTINATION "${INSTALL_PREFIX}/src"
        COMPONENT "sources")

install(DIRECTORY cmake_modules cpack_resources
        DESTINATION "${INSTALL_PREFIX}/src"
        COMPONENT "sources")


# package settings
set(CPACK_PACKAGE_NAME "${RTC_NAME}")
set(CPACK_PACKAGE_VERSION_MAJOR "${RTC_VERSION_MAJOR}")
set(CPACK_PACKAGE_VERSION_MINOR "${RTC_VERSION_MINOR}")
set(CPACK_PACKAGE_VERSION_PATCH "${RTC_VERSION_PATCH}")
set(CPACK_PACKAGE_VERSION "${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}")
set(CPACK_PACKAGE_VENDOR "${RTC_VENDOR}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${RTC_DESCRIPTION}")
set(CPACK_PACKAGE_CONTACT "${RTC_MAINTAINER}")

set(CPACK_RESOURCE_FILE_LICENSE
    "${CMAKE_CURRENT_SOURCE_DIR}/cpack_resources/License.txt")
set(CPACK_PACKAGE_DESCRIPTION_FILE
    "${CMAKE_CURRENT_SOURCE_DIR}/cpack_resources/Description.txt")

set(CPACK_COMPONENTS_ALL applications documents sources)
set(CPACK_COMPONENT_APPLICATIONS_DISPLAY_NAME "Applications")
set(CPACK_COMPONENT_APPLICATIONS_DESCRIPTION "RT-Component applications")
set(CPACK_COMPONENT_APPLICATIONS_DISABLED FALSE)

set(CPACK_COMPONENT_DOCUMENTS_DISPLAY_NAME "Documents")
set(CPACK_COMPONENT_DOCUMENTS_DESCRIPTION "RT-Component documents")
set(CPACK_COMPONENT_DOCUMENTS_DISABLED TRUE)

set(CPACK_COMPONENT_SOURCES_DISPLAY_NAME "Source files")
set(CPACK_COMPONENT_SOURCES_DESCRIPTION "RT-Component source files")
set(CPACK_COMPONENT_SOURCES_DISABLED TRUE)

if(WIN32)
    set(CPACK_GENERATOR "WIX")

    # Windows WiX package settings

    set(CPACK_WIX_XSL "@CMAKE_CURRENT_BINARY_DIR@/wix.xsl")
    set(CPACK_WIX_LANG "ja-jp")
    set(CPACK_RESOURCE_FILE_LICENSE
        "@CMAKE_CURRENT_SOURCE_DIR@/cpack_resources/License.rtf")
    configure_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/cpack_resources/wix.xsl.in"
        "${CMAKE_CURRENT_BINARY_DIR}/wix.xsl" @ONLY)

    set(CPACK_PACKAGE_FILE_NAME
        "rtc${OPENRTM_VERSION}-${PACKAGE_NAME}${PACKAGE_VERSION}")

else()
    set(CPACK_GENERATOR "${LINUX_PACKAGE_GENERATOR}")

    if(CPACK_GENERATOR STREQUAL "DEB")
        # Linux Debian package settings

        set(CPACK_DEBIAN_PACKAGE_VERSION "${CPACK_PACKAGE_VERSION}-1")
        set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "i386")
        set(CPACK_DEBIAN_PACKAGE_SECTION "main")
        set(CPACK_DEBIAN_PACKAGE_PRIORITY  "extra")
        set(CPACK_DEBIAN_PACKAGE_DEPENDS "openrtm-aist (>= 1.0.0)")

        set(CPACK_PACKAGE_FILE_NAME
            "rtc${OPENRTM_VERSION}-${PACKAGE_NAME}_${CPACK_DEBIAN_PACKAGE_VERSION}_${CPACK_DEBIAN_PACKAGE_ARCHITECTURE}")

    elseif(CPACK_GENERATOR STREQUAL "RPM")
        # Linux RPM package settings

        set(CPACK_RPM_PACKAGE_RELEASE "1.fc10")
        set(CPACK_RPM_PACKAGE_ARCHITECTURE "i386")
        set(CPACK_RPM_PACKAGE_GROUP "Development/Libraries")
        set(CPACK_RPM_PACKAGE_LICENSE "LGPL")
        set(CPACK_RPM_PACKAGE_REQUIRES "OpenRTM-aist >= 1.0.0")

        set(CPACK_PACKAGE_FILE_NAME
            "rtc${OPENRTM_VERSION}-${PACKAGE_NAME}-${PACKAGE_VERSION}-${CPACK_RPM_PACKAGE_RELEASE}.${CPACK_RPM_PACKAGE_ARCHITECTURE}")

    endif()
endif()

message(STATUS "Package type: ${CPACK_GENERATOR}")
message(STATUS "Package name: ${CPACK_PACKAGE_FILE_NAME}")

include(CPack)
