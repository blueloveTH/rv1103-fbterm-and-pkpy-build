#pragma once

#define PK_IS_PUBLIC_INCLUDE

#include "pocketpy/pocketpy.h"

#undef PK_IS_PUBLIC_INCLUDE

// inside config.h, near the top
#if !defined(__cplusplus)
    #ifndef static_assert
        #define static_assert _Static_assert
    #endif
#endif

