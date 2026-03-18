# Install script for directory: /Users/rowanterra/Desktop/phreeqc3_rrt/database

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/phreeqc/database" TYPE FILE FILES
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/Amm.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/ColdChem.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/Concrete_PHR.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/Concrete_PZ.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/core10.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/frezchem.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/iso.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/Kinec_v3.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/Kinec.v2.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/llnl.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/minteq.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/minteq.v4.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/phreeqc_rates.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/PHREEQC_ThermoddemV1.10_15Dec2020.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/phreeqc.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/pitzer.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/sit.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/stimela.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/Tipping_Hurley.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/database/wateq4f.dat"
    )
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/Users/rowanterra/Desktop/phreeqc3_rrt/build/database/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
