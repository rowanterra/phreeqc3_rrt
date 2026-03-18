# Install script for directory: /Users/rowanterra/Desktop/phreeqc3_rrt/examples

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/phreeqc/examples" TYPE FILE FILES
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/co2.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/co2.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/co2_VP.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex1"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex2"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex2b"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex2b.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex3"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex4"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex5"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex6"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex7"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex8"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex9"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex10"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex11"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex12"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex12a"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex12b"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex13a"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex13ac"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex13b"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex13c"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex14"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex15"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex15a"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex15b"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex15.dat"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex16"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex17"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex17b"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex18"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex19"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex19_meas.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex19b"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex20a"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex20b"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex20-c13.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex20-c14.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex21"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex21_Cl_tr_rad.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex21_Cs_rad.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex21_HTO_rad.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex21_Na_tr_rad.tsv"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/ex22"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/Zn1e_4"
    "/Users/rowanterra/Desktop/phreeqc3_rrt/examples/Zn1e_7"
    )
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/Users/rowanterra/Desktop/phreeqc3_rrt/build/examples/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
