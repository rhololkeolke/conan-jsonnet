cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
else()
  include(conanbuildinfo.cmake)
endif()
conan_basic_setup()

# necessary because conan package puts header in nlohmann subfolder,
# but jsonnet include "json.hpp" because that is how things are
# vendored inside the package.
include_directories("${CONAN_JSONFORMODERNCPP_ROOT}/include/nlohmann")

add_subdirectory("source_subfolder")

# Fixes https://github.com/google/jsonnet/issues/694
install(TARGETS md5
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib)
