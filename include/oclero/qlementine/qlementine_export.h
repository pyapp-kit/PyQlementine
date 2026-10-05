// Stand-in for the header upstream generates via CMake's generate_export_header.
// Qlementine is compiled statically into the Python extension, so no symbol
// import/export decoration is needed.
#pragma once

#define QLEMENTINE_EXPORT
#define QLEMENTINE_NO_EXPORT
