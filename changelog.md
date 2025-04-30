# Supported

## Breaking changes

- [#485](https://gitlab.com/libeigen/eigen/-/merge_requests/485): Removes deprecated CMake package config variables, potentially breaking existing CMake configurations
- [#608](https://gitlab.com/libeigen/eigen/-/merge_requests/608): Removes CI jobs for C++03 compatibility, signaling transition to modern C++ standards
- [#649](https://gitlab.com/libeigen/eigen/-/merge_requests/649): Move Eigen::all, last, and lastp1 back to Eigen::placeholders namespace to reduce name collision risks
- [#658](https://gitlab.com/libeigen/eigen/-/merge_requests/658): Refactored SVD module with new template parameter for computation options, breaking existing API
- [#725](https://gitlab.com/libeigen/eigen/-/merge_requests/725): Removed deprecated MappedSparseMatrix type from internal library code
- [#742](https://gitlab.com/libeigen/eigen/-/merge_requests/742): Updates minimum CMake version to 3.10, removes C++11 test disable option, and sets minimum GCC version to 5
- [#744](https://gitlab.com/libeigen/eigen/-/merge_requests/744): Updated compiler requirements by removing deprecated feature test macros and enforcing newer GCC and MSVC versions
- [#749](https://gitlab.com/libeigen/eigen/-/merge_requests/749): Reverts disruptive SVD module update that caused compatibility issues with third-party libraries
- [#771](https://gitlab.com/libeigen/eigen/-/merge_requests/771): Renamed internal `size` function to `ssize` to prevent ADL conflicts and improve C++ standard compatibility
- [#808](https://gitlab.com/libeigen/eigen/-/merge_requests/808): Introduces explicit type casting requirements for `pmadd` function to improve type safety and compatibility with custom scalar types
- [#826](https://gitlab.com/libeigen/eigen/-/merge_requests/826): Significant updates to SVD module with new Options template parameter, introducing API breaking changes for improved flexibility
- [#840](https://gitlab.com/libeigen/eigen/-/merge_requests/840): Fixed CUDA feature flag handling to respect `EIGEN_NO_CUDA` compilation option
- [#857](https://gitlab.com/libeigen/eigen/-/merge_requests/857): Reintroduced `svd::compute(Matrix, options)` method to prevent breaking external projects
- [#862](https://gitlab.com/libeigen/eigen/-/merge_requests/862): Restores fixed sizes for U/V matrices in matrix decompositions for fixed-sized inputs
- [#911](https://gitlab.com/libeigen/eigen/-/merge_requests/911): Fixed critical assumption about RowMajorBit and RowMajor, potentially impacting matrix storage order logic
- [#946](https://gitlab.com/libeigen/eigen/-/merge_requests/946): Removed legacy macro EIGEN_EMPTY_STRUCT_CTOR, potentially impacting older GCC compatibility
- [#966](https://gitlab.com/libeigen/eigen/-/merge_requests/966): Simplified Accelerate LLT and LDLT solvers by removing explicit Symmetric flag requirement

## Major changes

- [#356](https://gitlab.com/libeigen/eigen/-/merge_requests/356): Introduced PocketFFT as a more performant and accurate replacement for KissFFT in Eigen's FFT module
- [#489](https://gitlab.com/libeigen/eigen/-/merge_requests/489): Added AVX512 and AVX2 support for Packet16i and Packet8i, enhancing vectorization capabilities for integer types
- [#515](https://gitlab.com/libeigen/eigen/-/merge_requests/515): Adds random matrix generation via SVD with two strategies for generating singular values
- [#610](https://gitlab.com/libeigen/eigen/-/merge_requests/610): Updates CMake configuration to centralize C++11 standard setting, simplifying build process
- [#667](https://gitlab.com/libeigen/eigen/-/merge_requests/667): Significantly speeds up tensor reduction performance through loop strip mining and unrolling techniques
- [#673](https://gitlab.com/libeigen/eigen/-/merge_requests/673): Vectorized implementation of Visitor.h with up to 39% performance improvement using AVX2 instructions
- [#698](https://gitlab.com/libeigen/eigen/-/merge_requests/698): Optimizes `CommaInitializer` to reuse fixed dimensions more efficiently during matrix block initialization
- [#702](https://gitlab.com/libeigen/eigen/-/merge_requests/702): Added AVX vectorized implementation for float2half/half2float conversion functions with significant performance improvements
- [#732](https://gitlab.com/libeigen/eigen/-/merge_requests/732): Removes EIGEN_HAS_CXX11 macro, simplifying Eigen's codebase and focusing on C++11+ support
- [#736](https://gitlab.com/libeigen/eigen/-/merge_requests/736): SFINAE improvements for transpose methods in self-adjoint and triangular views
- [#764](https://gitlab.com/libeigen/eigen/-/merge_requests/764): Performance improvements for VSX and MMA GEMV operations on PowerPC, with up to 4X speedup
- [#796](https://gitlab.com/libeigen/eigen/-/merge_requests/796): Makes fixed-size Matrix and Array trivially copyable in C++20, improving memory management and compatibility
- [#817](https://gitlab.com/libeigen/eigen/-/merge_requests/817): Added support for int64 packets on x86 architectures, enabling more efficient vectorized operations
- [#820](https://gitlab.com/libeigen/eigen/-/merge_requests/820): Added reciprocal packet operation with optimized SSE, AVX, and AVX512 specializations for float, improving computational performance and accuracy
- [#824](https://gitlab.com/libeigen/eigen/-/merge_requests/824): Removed inline assembly for FMA (AVX) and added new packet operations pmsub, pnmadd, and pnmsub with performance improvements
- [#827](https://gitlab.com/libeigen/eigen/-/merge_requests/827): Optimized precipitation function implementation with IEEE compliance for 1/0 and 1/inf cases, improving performance and handling of special mathematical scenarios
- [#829](https://gitlab.com/libeigen/eigen/-/merge_requests/829): Replace Eigen type metaprogramming with standard C++ types and alias templates
- [#834](https://gitlab.com/libeigen/eigen/-/merge_requests/834): Introduces AVX512 optimized kernels for floating-point triangular solve operations, enhancing performance for smaller matrix sizes
- [#856](https://gitlab.com/libeigen/eigen/-/merge_requests/856): Adds support for Apple's Accelerate sparse matrix solvers with significant performance improvements for various factorization methods
- [#860](https://gitlab.com/libeigen/eigen/-/merge_requests/860): Adds AVX512 optimizations for matrix multiplication with significant performance improvements for single and double precision kernels
- [#868](https://gitlab.com/libeigen/eigen/-/merge_requests/868): Optimized SQRT/RSQRT implementations for modern x86 processors with improved performance and special value handling
- [#880](https://gitlab.com/libeigen/eigen/-/merge_requests/880): Fix critical SVD functionality bug for Microsoft Visual Studio (MSVC) compilation
- [#892](https://gitlab.com/libeigen/eigen/-/merge_requests/892): Added support for constant evaluation and improved alignment check assertions
- [#936](https://gitlab.com/libeigen/eigen/-/merge_requests/936): Performance improvements for GEMM on Power architecture with vector_pair loads and optimized matrix multiplication
- [#971](https://gitlab.com/libeigen/eigen/-/merge_requests/971): Introduces R-Bidiagonalization step to BDCSVD, optimizing SVD performance for tall and wide matrices using QR decomposition
- [#972](https://gitlab.com/libeigen/eigen/-/merge_requests/972): AVX512 optimizations for s/dgemm compute kernel, resolving previous architectural and build compatibility issues
- [#975](https://gitlab.com/libeigen/eigen/-/merge_requests/975): Introduced subMappers for Power GEMM packing, improving performance by approximately 10% through simplified address calculations
- [#983](https://gitlab.com/libeigen/eigen/-/merge_requests/983): Extends SYCL backend's QueueInterface to accept existing SYCL queues for improved framework integration
- [#986](https://gitlab.com/libeigen/eigen/-/merge_requests/986): SYCL-2020 range handling updated to ensure at least one thread execution by replacing default ranges with ranges of size 1
- [#990](https://gitlab.com/libeigen/eigen/-/merge_requests/990): Adds product operations and static initializers for DiagonalMatrix, improving matrix algebra convenience
- [#992](https://gitlab.com/libeigen/eigen/-/merge_requests/992): Enhanced AVX512 TRSM kernels to respect EIGEN_NO_MALLOC memory allocation configuration
- [#996](https://gitlab.com/libeigen/eigen/-/merge_requests/996): Updates SYCL kernel naming to comply with SYCL-2020 specification, improving SYCL compatibility and integration

## Other

### Fixed

- [#611](https://gitlab.com/libeigen/eigen/-/merge_requests/611): Included `<unordered_map>` header to resolve header inclusion issue
- [#613](https://gitlab.com/libeigen/eigen/-/merge_requests/613): Fix `fix<N>` implementation for environments without variable templates support
- [#614](https://gitlab.com/libeigen/eigen/-/merge_requests/614): Fixed LAPACK test compilation issues with type mismatches in older Fortran code
- [#621](https://gitlab.com/libeigen/eigen/-/merge_requests/621): Fixed GCC 4.8 ARM compilation issues by improving register constraints and resolving warnings
- [#628](https://gitlab.com/libeigen/eigen/-/merge_requests/628): Renamed 'vec_all_nan' symbol in cxx11_tensor_expr test to resolve build conflicts with altivec.h on ppc64le platform
- [#629](https://gitlab.com/libeigen/eigen/-/merge_requests/629): Fixed EIGEN_OPTIMIZATION_BARRIER compatibility for arm-clang compiler
- [#630](https://gitlab.com/libeigen/eigen/-/merge_requests/630): Fixed AVX2 integer packet issues and corrected AVX512 implementation details
- [#635](https://gitlab.com/libeigen/eigen/-/merge_requests/635): Fixed tridiagonalization selector issue by modifying `hCoeffs` vector handling to improve type compatibility
- [#638](https://gitlab.com/libeigen/eigen/-/merge_requests/638): Fixed missing packet types in pset1 function call, improving packet data handling robustness
- [#639](https://gitlab.com/libeigen/eigen/-/merge_requests/639): Fixed AVX2 PacketMath.h implementation with typo corrections and unaligned load resolution
- [#643](https://gitlab.com/libeigen/eigen/-/merge_requests/643): Minor fix for compilation error on HIP
- [#651](https://gitlab.com/libeigen/eigen/-/merge_requests/651): Remove `-fabi-version=6` flag from AVX512 builds to improve compatibility
- [#654](https://gitlab.com/libeigen/eigen/-/merge_requests/654): Silenced GCC string overflow warning in initializer_list_construction test
- [#656](https://gitlab.com/libeigen/eigen/-/merge_requests/656): Resolved strict aliasing bug causing product_small function failures in matrix multiplication
- [#657](https://gitlab.com/libeigen/eigen/-/merge_requests/657): Fixes implicit conversion warnings in tuple_test, improving type safety
- [#659](https://gitlab.com/libeigen/eigen/-/merge_requests/659): Fixed undefined behavior in BFloat16 float conversion by replacing `reinterpret_cast` with a safer alternative, improving reliability on PPC platforms
- [#664](https://gitlab.com/libeigen/eigen/-/merge_requests/664): Fixed MSVC compilation issues with complex compound assignment operators by disabling related tests
- [#665](https://gitlab.com/libeigen/eigen/-/merge_requests/665): Fix tuple compilation issues in Visual Studio 2017 by replacing tuple alias with TupleImpl
- [#666](https://gitlab.com/libeigen/eigen/-/merge_requests/666): Fixed MSVC+NVCC compilation issue with EIGEN_INHERIT_ASSIGNMENT_EQUAL_OPERATOR macro
- [#680](https://gitlab.com/libeigen/eigen/-/merge_requests/680): Fixed PowerPC packing issue, correcting row and depth inversion in non-vectorized code with 10% performance improvement
- [#686](https://gitlab.com/libeigen/eigen/-/merge_requests/686): Reverted bit_cast implementation to use memcpy for CUDA to prevent undefined behavior
- [#689](https://gitlab.com/libeigen/eigen/-/merge_requests/689): Fixed broadcasting index-out-of-bounds error for vectorized 1-dimensional inputs, particularly for std::complex types
- [#691](https://gitlab.com/libeigen/eigen/-/merge_requests/691): Fixed Clang warnings by replacing bitwise operators with correct logical operators
- [#694](https://gitlab.com/libeigen/eigen/-/merge_requests/694): Fixed ZVector build issues for s390x cross-compilation, enabling packetmath tests under QEMU
- [#696](https://gitlab.com/libeigen/eigen/-/merge_requests/696): Fixed build compatibility issues with pload and ploadu functions on ARM and PPC architectures by removing const from visitor return type
- [#703](https://gitlab.com/libeigen/eigen/-/merge_requests/703): Fix NaN propagation in min/max functions with scalar inputs
- [#707](https://gitlab.com/libeigen/eigen/-/merge_requests/707): Fixed total deflation issue in BDCSVD for diagonal matrices
- [#709](https://gitlab.com/libeigen/eigen/-/merge_requests/709): Fixed BDCSVD total deflation logic to correctly handle diagonal matrices
- [#711](https://gitlab.com/libeigen/eigen/-/merge_requests/711): Bug fix for incorrect definition of EIGEN_HAS_FP16_C macro across different compilers
- [#713](https://gitlab.com/libeigen/eigen/-/merge_requests/713): Prevent integer overflow in EigenMetaKernel indexing for improved reliability, especially on Windows builds
- [#714](https://gitlab.com/libeigen/eigen/-/merge_requests/714): Fixed uninitialized matrix issue to prevent potential computation errors
- [#719](https://gitlab.com/libeigen/eigen/-/merge_requests/719): Fixed Sparse-Sparse product implementation for mixed StorageIndex types
- [#728](https://gitlab.com/libeigen/eigen/-/merge_requests/728): Fixed compilation errors for Windows build systems
- [#733](https://gitlab.com/libeigen/eigen/-/merge_requests/733): Fixed warnings about shadowing definitions to improve code clarity and maintainability
- [#741](https://gitlab.com/libeigen/eigen/-/merge_requests/741): Fixes HIP compilation failure in DenseBase by adding appropriate EIGEN_DEVICE_FUNC modifiers
- [#745](https://gitlab.com/libeigen/eigen/-/merge_requests/745): Fixed HIP compilation issues in selfAdjoint and triangular view classes
- [#746](https://gitlab.com/libeigen/eigen/-/merge_requests/746): Fixed handling of 0-sized matrices in LAPACKE-based Cholesky decomposition
- [#759](https://gitlab.com/libeigen/eigen/-/merge_requests/759): Fixed typo of `StableNorm` to `stableNorm` in IDRS.h file
- [#762](https://gitlab.com/libeigen/eigen/-/merge_requests/762): Fixed documentation code snippets to improve accuracy and readability
- [#765](https://gitlab.com/libeigen/eigen/-/merge_requests/765): Resolved Clang compiler ambiguity in index list overloads to improve code stability
- [#769](https://gitlab.com/libeigen/eigen/-/merge_requests/769): Fixed header inclusion issues in CholmodSupport to prevent direct access to internal files
- [#782](https://gitlab.com/libeigen/eigen/-/merge_requests/782): Fix a bug with the EIGEN_IMPLIES macro's side-effects introduced in a previous merge request
- [#785](https://gitlab.com/libeigen/eigen/-/merge_requests/785): Fixed Clang warnings related to alignment and floating-point precision
- [#789](https://gitlab.com/libeigen/eigen/-/merge_requests/789): Fixed inclusion of immintrin.h for F16C intrinsics when vectorization is disabled
- [#794](https://gitlab.com/libeigen/eigen/-/merge_requests/794): Fixed header guard conflicts between AltiVec and ZVector packages
- [#800](https://gitlab.com/libeigen/eigen/-/merge_requests/800): Fixes serialization API issues disrupting HIP GPU unit tests
- [#801](https://gitlab.com/libeigen/eigen/-/merge_requests/801): Fixes and cleanups for BFloat16 and Half numeric_limits, including AVX `psqrt` function workaround
- [#802](https://gitlab.com/libeigen/eigen/-/merge_requests/802): Fixed improper truncation of unsigned int to bool, improving type conversion reliability
- [#803](https://gitlab.com/libeigen/eigen/-/merge_requests/803): Fixed GCC 8.5 warning about missing base class initialization
- [#805](https://gitlab.com/libeigen/eigen/-/merge_requests/805): Fixed inconsistency in scalar and vectorized paths for array.exp() function
- [#806](https://gitlab.com/libeigen/eigen/-/merge_requests/806): Fix assertion messages in IterativeSolverBase to correctly reference its own class name
- [#809](https://gitlab.com/libeigen/eigen/-/merge_requests/809): Fixed broken assertions to improve runtime error checking and library reliability
- [#810](https://gitlab.com/libeigen/eigen/-/merge_requests/810): Fixed two corner cases in logistic sigmoid implementation for improved accuracy and robustness
- [#811](https://gitlab.com/libeigen/eigen/-/merge_requests/811): Fixed compilation issue with GCC < 10 and -std=c++2a standard
- [#812](https://gitlab.com/libeigen/eigen/-/merge_requests/812): Fix implicit conversion warning in vectorwise_reverse_inplace function by adding explicit casting
- [#815](https://gitlab.com/libeigen/eigen/-/merge_requests/815): Fixed implicit conversion warning in GEBP kernel's packing by changing variable types from `int` to `Index`
- [#818](https://gitlab.com/libeigen/eigen/-/merge_requests/818): Silenced specific MSVC compiler warnings in `construct_elements_of_array()` function
- [#822](https://gitlab.com/libeigen/eigen/-/merge_requests/822): Fixed potential overflow issue in random test by making casts explicit and adjusting variable types
- [#828](https://gitlab.com/libeigen/eigen/-/merge_requests/828): Fixed GEMV cache overflow issue for PowerPC architecture
- [#833](https://gitlab.com/libeigen/eigen/-/merge_requests/833): Fixes type discrepancy in 32-bit ARM platforms by replacing `int` with `int32_t` for proper bit pattern extraction
- [#835](https://gitlab.com/libeigen/eigen/-/merge_requests/835): Fixed ODR violations by removing unnamed namespaces and internal linkage from header files
- [#842](https://gitlab.com/libeigen/eigen/-/merge_requests/842): Fixed documentation typo in Complete Orthogonal Decomposition (COD) method reference
- [#843](https://gitlab.com/libeigen/eigen/-/merge_requests/843): Fixed naming collision with resolve.h by renaming local variables
- [#847](https://gitlab.com/libeigen/eigen/-/merge_requests/847): Cleaned up compiler warnings for PowerPC GEMM and GEMV implementations
- [#851](https://gitlab.com/libeigen/eigen/-/merge_requests/851): Fixed JacobiSVD_LAPACKE bindings to align with SVD module runtime options
- [#858](https://gitlab.com/libeigen/eigen/-/merge_requests/858): Fixed sqrt/rsqrt implementations for NEON with improved accuracy and special case handling
- [#859](https://gitlab.com/libeigen/eigen/-/merge_requests/859): Fixed MSVC+NVCC 9.2 pragma compatibility issue by replacing `_Pragma` with `__pragma`
- [#863](https://gitlab.com/libeigen/eigen/-/merge_requests/863): Modified test expression to avoid numerical differences during optimization
- [#865](https://gitlab.com/libeigen/eigen/-/merge_requests/865): Added assertion for edge case when requesting thin unitaries with incompatible matrix dimensions
- [#866](https://gitlab.com/libeigen/eigen/-/merge_requests/866): Fix crash bug in SPQRSupport by initializing pointers to nullptr to prevent invalid memory access
- [#870](https://gitlab.com/libeigen/eigen/-/merge_requests/870): Fixed test macro conflicts with STL headers in C++20 for GCC 9-11
- [#873](https://gitlab.com/libeigen/eigen/-/merge_requests/873): Disabled deprecated warnings in SVD tests to clean up build logs
- [#874](https://gitlab.com/libeigen/eigen/-/merge_requests/874): Fixed gcc-5 packetmath_12 bug with memory initialization in `packetmath_minus_zero_add()`
- [#875](https://gitlab.com/libeigen/eigen/-/merge_requests/875): Fixed compilation error in packetmath by introducing a wrapper struct for `psqrt` function
- [#876](https://gitlab.com/libeigen/eigen/-/merge_requests/876): Fixed AVX512 instruction handling and complex type computation issues for g++-11
- [#877](https://gitlab.com/libeigen/eigen/-/merge_requests/877): Disabled deprecated warnings for SVD tests on MSVC to improve build log clarity
- [#878](https://gitlab.com/libeigen/eigen/-/merge_requests/878): Fixed frexp packetmath tests for MSVC to handle non-finite input exponent behavior
- [#882](https://gitlab.com/libeigen/eigen/-/merge_requests/882): Fixed SVD compatibility issues for MSVC and CUDA by resolving Index type and function return warnings
- [#883](https://gitlab.com/libeigen/eigen/-/merge_requests/883): Adjusted matrix_power test tolerance for MSVC to reduce test failures
- [#885](https://gitlab.com/libeigen/eigen/-/merge_requests/885): Fixed enum conversion warnings in BooleanRedux component
- [#886](https://gitlab.com/libeigen/eigen/-/merge_requests/886): Fixed denormal test to skip when condition is false
- [#900](https://gitlab.com/libeigen/eigen/-/merge_requests/900): Fix swap test for size 1 matrix inputs to prevent assertion failures
- [#901](https://gitlab.com/libeigen/eigen/-/merge_requests/901): Fixed `construct_at` compilation issue on ROCm/HIP environments
- [#908](https://gitlab.com/libeigen/eigen/-/merge_requests/908): Corrected reference code for `ata_product` function in STL_interface.hh
- [#910](https://gitlab.com/libeigen/eigen/-/merge_requests/910): Reverted previous changes to PowerPC MMA flags to restore stability
- [#914](https://gitlab.com/libeigen/eigen/-/merge_requests/914): Disabled Schur non-convergence test to reduce flaky results and improve reliability
- [#915](https://gitlab.com/libeigen/eigen/-/merge_requests/915): Fixed missing pound directive to improve compilation and code robustness
- [#917](https://gitlab.com/libeigen/eigen/-/merge_requests/917): Resolved g++-10 docker compiler optimization issue in geo_orthomethods_4 test
- [#918](https://gitlab.com/libeigen/eigen/-/merge_requests/918): Added missing explicit reinterprets for `_mm512_shuffle_f32x4` to resolve g++ build errors
- [#919](https://gitlab.com/libeigen/eigen/-/merge_requests/919): Fixed a missing parenthesis in the tutorial documentation
- [#922](https://gitlab.com/libeigen/eigen/-/merge_requests/922): Work around MSVC compiler bug dropping `const` qualifier in method definitions
- [#923](https://gitlab.com/libeigen/eigen/-/merge_requests/923): Fixed AVX512 build compatibility issues with MSVC compiler
- [#924](https://gitlab.com/libeigen/eigen/-/merge_requests/924): Disabled f16c scalar conversions for MSVC to prevent compatibility issues
- [#925](https://gitlab.com/libeigen/eigen/-/merge_requests/925): Fixed ODR violation in trsm module by marking specific functions as inline
- [#926](https://gitlab.com/libeigen/eigen/-/merge_requests/926): Fixed compilation errors by correcting namespace usage in the codebase
- [#930](https://gitlab.com/libeigen/eigen/-/merge_requests/930): Fixed compilation issue in GCC 9 by adding missing typename and removing unused typedef
- [#934](https://gitlab.com/libeigen/eigen/-/merge_requests/934): Fixed order of arguments in BLAS SYRK implementation to resolve compilation errors
- [#937](https://gitlab.com/libeigen/eigen/-/merge_requests/937): Eliminates warnings related to unused trace statements, improving code cleanliness
- [#945](https://gitlab.com/libeigen/eigen/-/merge_requests/945): Restored correct max size expressions that were unintentionally modified in a previous merge request
- [#948](https://gitlab.com/libeigen/eigen/-/merge_requests/948): Fix compatibility issues between MSVC and CUDA for diagonal and transpose functionality
- [#949](https://gitlab.com/libeigen/eigen/-/merge_requests/949): Fixed ODR violations in lapacke_helpers module to improve library reliability
- [#953](https://gitlab.com/libeigen/eigen/-/merge_requests/953): Fixed ambiguous constructors for DiagonalMatrix to prevent compile-time errors with initializer lists
- [#958](https://gitlab.com/libeigen/eigen/-/merge_requests/958): Fixed compiler bugs for GCC 10 & 11 in Power GEMM inline assembly
- [#963](https://gitlab.com/libeigen/eigen/-/merge_requests/963): Fixed NaN propagation for scalar input by adding missing template parameter
- [#964](https://gitlab.com/libeigen/eigen/-/merge_requests/964): Fix compilation issue in HouseholderSequence.h related to InnerPanel template parameter
- [#974](https://gitlab.com/libeigen/eigen/-/merge_requests/974): Fixed BDCSVD crash caused by index out of bounds in matrix processing
- [#976](https://gitlab.com/libeigen/eigen/-/merge_requests/976): Fix LDLT decomposition with AutoDiffScalar when value is 0
- [#977](https://gitlab.com/libeigen/eigen/-/merge_requests/977): Fixed numerical stability issue in BDCSVD algorithm
- [#980](https://gitlab.com/libeigen/eigen/-/merge_requests/980): Fixed signed integer overflow in adjoint test to improve code safety
- [#987](https://gitlab.com/libeigen/eigen/-/merge_requests/987): Fixed integer shortening warnings in visitor tests
- [#988](https://gitlab.com/libeigen/eigen/-/merge_requests/988): Fixed MSVC build issues with AVX512 by temporarily disabling specific optimizations to reduce memory consumption and prevent compilation failures
- [#991](https://gitlab.com/libeigen/eigen/-/merge_requests/991): Resolved ambiguous comparison warnings in clang for C++20 by adjusting TensorBase comparison operators
- [#993](https://gitlab.com/libeigen/eigen/-/merge_requests/993): Corrected row vs column vector terminology typo in Matrix class tutorial documentation
- [#1003](https://gitlab.com/libeigen/eigen/-/merge_requests/1003): Eliminated undefined warnings for non-AVX512 compilation by adding appropriate macro guards
- [#1007](https://gitlab.com/libeigen/eigen/-/merge_requests/1007): Fixed One Definition Rule (ODR) violations by converting unnamed type declarations to named types

### Improved

- [#544](https://gitlab.com/libeigen/eigen/-/merge_requests/544): Added GDB pretty printer support for Eigen::Block types to improve debugging experience
- [#572](https://gitlab.com/libeigen/eigen/-/merge_requests/572): Removed unnecessary `const` qualifiers from AutodiffScalar return types to improve code quality and readability
- [#605](https://gitlab.com/libeigen/eigen/-/merge_requests/605): Updated SparseExtra RandomSetter to use unordered_map for improved performance
- [#609](https://gitlab.com/libeigen/eigen/-/merge_requests/609): Optimize predux, predux_min, and predux_max operations for AArch64 architecture using specialized intrinsics
- [#615](https://gitlab.com/libeigen/eigen/-/merge_requests/615): Adds intrin header for Windows ARM to improve compatibility and intrinsic function support
- [#617](https://gitlab.com/libeigen/eigen/-/merge_requests/617): Extended matrixmarket reader/writer to support handling of dense matrices
- [#618](https://gitlab.com/libeigen/eigen/-/merge_requests/618): Added EIGEN_DEVICE_FUNC labels to improve CUDA 9 compatibility for gpu_basic tests
- [#631](https://gitlab.com/libeigen/eigen/-/merge_requests/631): Introduced error handling to prevent direct inclusion of internal Eigen headers
- [#632](https://gitlab.com/libeigen/eigen/-/merge_requests/632): Simplified CMake configuration by removing unused interface definitions
- [#633](https://gitlab.com/libeigen/eigen/-/merge_requests/633): Simplified CMake versioning for architecture-independent package configurations using `ARCH_INDEPENDENT` option
- [#634](https://gitlab.com/libeigen/eigen/-/merge_requests/634): Improved CMake package registry configuration for better dependency management
- [#641](https://gitlab.com/libeigen/eigen/-/merge_requests/641): Removed unnecessary std::tuple reference to simplify codebase
- [#647](https://gitlab.com/libeigen/eigen/-/merge_requests/647): Cleaned up EIGEN_STATIC_ASSERT to use standard C++11 static_assert, improving error messages and code organization
- [#648](https://gitlab.com/libeigen/eigen/-/merge_requests/648): Corrected typographical errors in copyright dates across project files
- [#652](https://gitlab.com/libeigen/eigen/-/merge_requests/652): Added a macro to pass arguments to ctest for running tests in parallel
- [#655](https://gitlab.com/libeigen/eigen/-/merge_requests/655): Improved CI test execution by running tests in parallel across all available CPU cores
- [#660](https://gitlab.com/libeigen/eigen/-/merge_requests/660): Corrected multiple typos in documentation and comments to improve code clarity and readability
- [#661](https://gitlab.com/libeigen/eigen/-/merge_requests/661): Corrected typographical errors in documentation and code comments
- [#662](https://gitlab.com/libeigen/eigen/-/merge_requests/662): Reorganized test main file for improved maintainability and code structure
- [#663](https://gitlab.com/libeigen/eigen/-/merge_requests/663): Reduced CUDA compilation warnings for versions 9.2 and 11.4
- [#668](https://gitlab.com/libeigen/eigen/-/merge_requests/668): Updated CMake Windows compiler and OS detection with more reliable and maintainable methods
- [#677](https://gitlab.com/libeigen/eigen/-/merge_requests/677): Optimized type punning in CUDA code by replacing memcpy with reinterpret_cast for improved GPU performance
- [#687](https://gitlab.com/libeigen/eigen/-/merge_requests/687): Adds nan-propagation options to elementwise min/max operations and reductions in matrix and array plugins
- [#692](https://gitlab.com/libeigen/eigen/-/merge_requests/692): Extend Eigen's Qt support to Qt6 by modifying compatibility functions in Transform.h
- [#693](https://gitlab.com/libeigen/eigen/-/merge_requests/693): Enhanced documentation for Stride class inner stride behavior in compile-time vectors
- [#697](https://gitlab.com/libeigen/eigen/-/merge_requests/697): Optimize CMake scripts to improve Eigen subproject integration and reduce default test build overhead
- [#700](https://gitlab.com/libeigen/eigen/-/merge_requests/700): Vectorized tanh and logistic functions for fp16 on Neon, improving computational performance
- [#701](https://gitlab.com/libeigen/eigen/-/merge_requests/701): Move alignment qualifier to improve consistency and resolve compiler warnings
- [#712](https://gitlab.com/libeigen/eigen/-/merge_requests/712): Improved documentation for Quaternion constructor from MatrixBase, clarifying element order and usage
- [#716](https://gitlab.com/libeigen/eigen/-/merge_requests/716): Converted diagnostic pragmas to standardized nv_diag format, improving code consistency and maintainability
- [#717](https://gitlab.com/libeigen/eigen/-/merge_requests/717): Moved pruning code from CompressedStorage to SparseVector.h to improve code organization
- [#718](https://gitlab.com/libeigen/eigen/-/merge_requests/718): Update SparseMatrix::Map and TransposedSparseMatrix to use consistent StorageIndex across implementations
- [#720](https://gitlab.com/libeigen/eigen/-/merge_requests/720): Fixed a documentation typo to improve clarity
- [#722](https://gitlab.com/libeigen/eigen/-/merge_requests/722): Optimized Umeyama algorithm computation by conditionally skipping unnecessary scaling calculations
- [#726](https://gitlab.com/libeigen/eigen/-/merge_requests/726): Added basic iterator support for Eigen::array to simplify array usage and transition from std::array
- [#727](https://gitlab.com/libeigen/eigen/-/merge_requests/727): Made numeric_limits members constexpr for improved compile-time evaluation
- [#734](https://gitlab.com/libeigen/eigen/-/merge_requests/734): Improved AVX2 optimization selection for non-multiple-of-8 data sizes
- [#735](https://gitlab.com/libeigen/eigen/-/merge_requests/735): Simplified C++11 feature checks by removing redundant macros and compiler version checks
- [#737](https://gitlab.com/libeigen/eigen/-/merge_requests/737): Refactored Lapacke LLT macro binding to improve code clarity and maintainability
- [#748](https://gitlab.com/libeigen/eigen/-/merge_requests/748): Improved Lapacke bindings for HouseholderQR and PartialPivLU by replacing macros with C++ code and extracting common binding logic
- [#753](https://gitlab.com/libeigen/eigen/-/merge_requests/753): Convert computational macros to type-safe constexpr functions for improved code quality
- [#756](https://gitlab.com/libeigen/eigen/-/merge_requests/756): Conditional inclusion of <atomic> header to improve compatibility with toolchains lacking atomic operations support
- [#757](https://gitlab.com/libeigen/eigen/-/merge_requests/757): Refactored IDRS code, replacing `norm()` with `StableNorm()` to improve code stability and numerical performance
- [#760](https://gitlab.com/libeigen/eigen/-/merge_requests/760): Removed `using namespace Eigen` from sample code to promote better coding practices
- [#761](https://gitlab.com/libeigen/eigen/-/merge_requests/761): Cleanup of obsolete compiler checks and flags, streamlining the codebase and reducing maintenance overhead
- [#763](https://gitlab.com/libeigen/eigen/-/merge_requests/763): Cleaned up CMake scripts by removing deprecated `COMPILE_FLAGS` and adopting modern `target_compile_options`
- [#767](https://gitlab.com/libeigen/eigen/-/merge_requests/767): Improved `exp()` function behavior for `-Inf` arguments in vectorized expressions with performance optimizations
- [#772](https://gitlab.com/libeigen/eigen/-/merge_requests/772): Cleanup of internal macros and sequence implementations to simplify codebase
- [#773](https://gitlab.com/libeigen/eigen/-/merge_requests/773): Optimized row-major sparse-dense matrix product implementation with two accumulation variables to improve computational efficiency
- [#774](https://gitlab.com/libeigen/eigen/-/merge_requests/774): Fixes for enabling HIP unit tests and updating CMake compatibility
- [#776](https://gitlab.com/libeigen/eigen/-/merge_requests/776): Improved CMake handling of `EIGEN_TEST_CUSTOM_CXX_FLAGS` by converting spaces to semicolons
- [#779](https://gitlab.com/libeigen/eigen/-/merge_requests/779): Optimize `exp<float>()` with reduced polynomial degree, expanded denormal range, and 4% speedup for AVX2
- [#780](https://gitlab.com/libeigen/eigen/-/merge_requests/780): Improved accuracy and performance of logistic sigmoid function implementation, reducing maximum relative error and extending computational range
- [#783](https://gitlab.com/libeigen/eigen/-/merge_requests/783): Simplified `logical_xor()` implementation for bool types, improving code clarity and efficiency
- [#786](https://gitlab.com/libeigen/eigen/-/merge_requests/786): Small cleanup of GDB pretty printer code, improving code readability and maintenance
- [#788](https://gitlab.com/libeigen/eigen/-/merge_requests/788): Small documentation and code quality improvements, including fixing warnings and documentation formatting
- [#790](https://gitlab.com/libeigen/eigen/-/merge_requests/790): Added missing internal namespace qualifiers to vectorization logic tests
- [#791](https://gitlab.com/libeigen/eigen/-/merge_requests/791): Added support for Cray, Fujitsu, and Intel ICX compilers with new preprocessor macros
- [#792](https://gitlab.com/libeigen/eigen/-/merge_requests/792): Enables manual specification of inner and outer strides for CWiseUnaryView, enhancing stride control and flexibility
- [#795](https://gitlab.com/libeigen/eigen/-/merge_requests/795): Refactored identifiers to reduce usage of reserved names in compliance with C++ standard guidelines
- [#797](https://gitlab.com/libeigen/eigen/-/merge_requests/797): Adds bounds checking to Eigen serializer to improve data integrity and prevent out-of-bounds access
- [#799](https://gitlab.com/libeigen/eigen/-/merge_requests/799): Performance improvement for logarithm function with 20% speedup for float and better denormal handling
- [#813](https://gitlab.com/libeigen/eigen/-/merge_requests/813): Corrected and clarified documentation for Least Squares Conjugate Gradient (LSCG) solver, improving mathematical descriptions and user understanding
- [#814](https://gitlab.com/libeigen/eigen/-/merge_requests/814): Updated comments to remove references to outdated macro and improve code clarity
- [#816](https://gitlab.com/libeigen/eigen/-/merge_requests/816): Port EIGEN_OPTIMIZATION_BARRIER to support soft float ARM architectures
- [#819](https://gitlab.com/libeigen/eigen/-/merge_requests/819): Enhance clang warning suppressions by checking for supported warnings before applying suppressions
- [#821](https://gitlab.com/libeigen/eigen/-/merge_requests/821): Prevent unnecessary heap allocation in diagonal product by setting NestByRefBit for more efficient memory management
- [#825](https://gitlab.com/libeigen/eigen/-/merge_requests/825): Introduced utility functions to reduce floating-point warnings and improve comparison precision
- [#830](https://gitlab.com/libeigen/eigen/-/merge_requests/830): Removed documentation referencing obsolete C++98/C++03 standards
- [#832](https://gitlab.com/libeigen/eigen/-/merge_requests/832): Improved AVX512 math function consistency and ICC compatibility for more reliable mathematical computations
- [#836](https://gitlab.com/libeigen/eigen/-/merge_requests/836): Refined compiler-specific `maxpd` workaround to target only GCC<6.3
- [#838](https://gitlab.com/libeigen/eigen/-/merge_requests/838): Corrected definition of EIGEN_HAS_AVX512_MATH in PacketMath to improve AVX512 math capabilities
- [#841](https://gitlab.com/libeigen/eigen/-/merge_requests/841): Consolidated and improved generic implementations of psqrt and prsqrt functions with correct handling of special cases
- [#844](https://gitlab.com/libeigen/eigen/-/merge_requests/844): Updated MPL2 license link to use HTTPS for improved security
- [#845](https://gitlab.com/libeigen/eigen/-/merge_requests/845): Improved numeric_limits implementation to ensure One Definition Rule (ODR) compliance and enhance static data member definitions
- [#846](https://gitlab.com/libeigen/eigen/-/merge_requests/846): Optimize performance by returning alphas() and betas() vectors as const references
- [#849](https://gitlab.com/libeigen/eigen/-/merge_requests/849): Improved documentation for MatrixXNt and MatrixNXt matrix patterns and fixed documentation compilation issues
- [#850](https://gitlab.com/libeigen/eigen/-/merge_requests/850): Added descriptive comments to Matrix typedefs to improve Doxygen documentation
- [#854](https://gitlab.com/libeigen/eigen/-/merge_requests/854): Added scaling function overload to handle vector rvalue references, improving diagonal matrix creation from temporary vectors
- [#861](https://gitlab.com/libeigen/eigen/-/merge_requests/861): Improved FixedInt constexpr support and resolved potential ODR violations
- [#864](https://gitlab.com/libeigen/eigen/-/merge_requests/864): Cleaned up unnecessary EIGEN_UNUSED decorations to improve code clarity and maintainability
- [#869](https://gitlab.com/libeigen/eigen/-/merge_requests/869): Improved SYCL support by simplifying CMake configuration and enhancing compatibility with C++ versions
- [#872](https://gitlab.com/libeigen/eigen/-/merge_requests/872): Improved sqrt/rsqrt handling of denormal numbers and performance optimizations for AVX512
- [#879](https://gitlab.com/libeigen/eigen/-/merge_requests/879): Improved efficiency of any/all reduction operations for row-major matrix layouts
- [#884](https://gitlab.com/libeigen/eigen/-/merge_requests/884): Simplified non-convergence checks in NonLinearOptimization tests to improve test reliability across different architectures
- [#887](https://gitlab.com/libeigen/eigen/-/merge_requests/887): Enhance vectorization logic tests for improved cross-platform compatibility and test reliability
- [#888](https://gitlab.com/libeigen/eigen/-/merge_requests/888): Optimized least_square_conjugate_gradient() performance using .noalias() to reduce temporary allocations
- [#889](https://gitlab.com/libeigen/eigen/-/merge_requests/889): Introduced `construct_at` and `destroy_at` wrappers, improving code clarity and modernizing memory management practices throughout Eigen
- [#890](https://gitlab.com/libeigen/eigen/-/merge_requests/890): Removed duplicate IsRowMajor declaration to reduce compilation warnings and improve code clarity
- [#891](https://gitlab.com/libeigen/eigen/-/merge_requests/891): Optimized SVD test memory consumption by splitting and reducing test matrix sizes
- [#893](https://gitlab.com/libeigen/eigen/-/merge_requests/893): Adds new CMake configuration options for more flexible build control of Eigen library components
- [#895](https://gitlab.com/libeigen/eigen/-/merge_requests/895): Added move constructors to SparseSolverBase and IterativeSolverBase for improved solver object management
- [#903](https://gitlab.com/libeigen/eigen/-/merge_requests/903): Replaces enum with constexpr for floating point bit size calculations, reducing type casts and improving code readability
- [#904](https://gitlab.com/libeigen/eigen/-/merge_requests/904): Converted static const class members to constexpr for improved compile-time efficiency
- [#907](https://gitlab.com/libeigen/eigen/-/merge_requests/907): Enhances PowerPC MMA build options with dynamic dispatch and improved compatibility for Power10 processors
- [#909](https://gitlab.com/libeigen/eigen/-/merge_requests/909): Removed outdated GCC-4 warning workarounds, simplifying and improving code maintainability
- [#913](https://gitlab.com/libeigen/eigen/-/merge_requests/913): PowerPC MMA build configuration enhancement with dynamic dispatch option
- [#916](https://gitlab.com/libeigen/eigen/-/merge_requests/916): Updated Altivec MMA dynamic dispatch flags to support binary values for improved TensorFlow compatibility
- [#921](https://gitlab.com/libeigen/eigen/-/merge_requests/921): Optimized visitor traversal for RowMajor inputs, improving matrix operation performance
- [#927](https://gitlab.com/libeigen/eigen/-/merge_requests/927): Update warning suppression techniques for improved compiler compatibility
- [#929](https://gitlab.com/libeigen/eigen/-/merge_requests/929): Split general matrix-vector product interface for Power architectures to improve TensorFlow compatibility
- [#931](https://gitlab.com/libeigen/eigen/-/merge_requests/931): Re-enabled Aarch64 CI pipelines to improve testing and validation for Aarch64 architecture
- [#939](https://gitlab.com/libeigen/eigen/-/merge_requests/939): Improved LAPACK module code organization by removing `.cpp` file inclusions
- [#940](https://gitlab.com/libeigen/eigen/-/merge_requests/940): Reintroduced std::remove* aliases to restore compatibility with third-party libraries
- [#941](https://gitlab.com/libeigen/eigen/-/merge_requests/941): Improve scalar test_isApprox handling of inf/nan values
- [#943](https://gitlab.com/libeigen/eigen/-/merge_requests/943): Enhanced `constexpr` helper functions in `XprHelper.h` to improve compile-time computations and code clarity
- [#944](https://gitlab.com/libeigen/eigen/-/merge_requests/944): Converted metaprogramming utility to constexpr function for improved compile-time evaluation and code simplification
- [#947](https://gitlab.com/libeigen/eigen/-/merge_requests/947): Added partial loading, storing, gathering, and scattering packet operations to improve memory access efficiency and performance
- [#951](https://gitlab.com/libeigen/eigen/-/merge_requests/951): Optimized Power GEMV predux operations for MMA, reducing instruction count and improving compatibility with GCC
- [#952](https://gitlab.com/libeigen/eigen/-/merge_requests/952): Introduced workarounds to allow all tests to pass with `EIGEN_TEST_NO_EXPLICIT_VECTORIZATION` setting
- [#959](https://gitlab.com/libeigen/eigen/-/merge_requests/959): Improved AVX512 implementation with header file renaming and hardware capability restrictions
- [#960](https://gitlab.com/libeigen/eigen/-/merge_requests/960): Removed AVX512VL dependency in trsm function, improving compatibility across different AVX configurations
- [#962](https://gitlab.com/libeigen/eigen/-/merge_requests/962): Optimized Householder sequence block handling to eliminate unnecessary heap allocations and improve performance
- [#967](https://gitlab.com/libeigen/eigen/-/merge_requests/967): Optimized GEMM MMA with vector_pairs loading and improved predux GEMV performance
- [#968](https://gitlab.com/libeigen/eigen/-/merge_requests/968): Made diagonal matrix `cols()` and `rows()` methods constexpr to improve compile-time evaluation
- [#969](https://gitlab.com/libeigen/eigen/-/merge_requests/969): Conditionally add `uninstall` target to prevent CMake installation conflicts
- [#984](https://gitlab.com/libeigen/eigen/-/merge_requests/984): Removes executable flag from files to improve project file permission management
- [#985](https://gitlab.com/libeigen/eigen/-/merge_requests/985): Improved logical shift operation implementations and fixed typo in SVE/PacketMath.h
- [#989](https://gitlab.com/libeigen/eigen/-/merge_requests/989): Resolves C++20 comparison operator ambiguity in template comparisons
- [#994](https://gitlab.com/libeigen/eigen/-/merge_requests/994): Marks `index_remap` as `EIGEN_DEVICE_FUNC` to enable GPU expression reshaping
- [#997](https://gitlab.com/libeigen/eigen/-/merge_requests/997): Enhances AVX512 TRSM kernels memory management by using `alloca` when `EIGEN_NO_MALLOC` is requested
- [#998](https://gitlab.com/libeigen/eigen/-/merge_requests/998): Improved tanh and erf vectorized implementation for EIGEN_FAST_MATH in VSX architecture
- [#999](https://gitlab.com/libeigen/eigen/-/merge_requests/999): Update Householder.h to use numext::sqrt for improved custom type support
- [#1000](https://gitlab.com/libeigen/eigen/-/merge_requests/1000): Performance optimization for GEMV on Power10 architecture using more load and store vector pairs
- [#1002](https://gitlab.com/libeigen/eigen/-/merge_requests/1002): Addressed clang-tidy warnings by reformatting function definitions in headers and improving code clarity

### Added

- [#121](https://gitlab.com/libeigen/eigen/-/merge_requests/121): Added a `make format` command to enforce consistent code styling across the project
- [#447](https://gitlab.com/libeigen/eigen/-/merge_requests/447): Introduces BiCGSTAB(L) algorithm for solving linear systems with potential improvements for non-symmetric systems
- [#482](https://gitlab.com/libeigen/eigen/-/merge_requests/482): Adds LLDB synthetic child provider for structured display of Eigen matrices and vectors during debugging
- [#646](https://gitlab.com/libeigen/eigen/-/merge_requests/646): Added new make targets `buildtests_gpu` and `check_gpu` to simplify GPU testing infrastructure
- [#688](https://gitlab.com/libeigen/eigen/-/merge_requests/688): Added nan-propagation options to matrix and array plugins for enhanced NaN value handling
- [#729](https://gitlab.com/libeigen/eigen/-/merge_requests/729): Implemented `reverse_iterator` for `Eigen::array<...>` to enhance iteration capabilities
- [#758](https://gitlab.com/libeigen/eigen/-/merge_requests/758): Added GPU unit tests for HIP using C++14, improving testing for GPU functionalities
- [#852](https://gitlab.com/libeigen/eigen/-/merge_requests/852): Adds convenience `constexpr std::size_t size() const` method to `Eigen::IndexList`
- [#965](https://gitlab.com/libeigen/eigen/-/merge_requests/965): Added three new fused multiply functions (pmsub, pnmadd, pnmsub) for PowerPC architecture
- [#981](https://gitlab.com/libeigen/eigen/-/merge_requests/981): Added MKL adapter and implementations for KFR and FFTS FFT libraries in Eigen's FFT module
- [#995](https://gitlab.com/libeigen/eigen/-/merge_requests/995): Added comprehensive documentation for the DiagonalBase class to improve library usability

### Removed

- [#636](https://gitlab.com/libeigen/eigen/-/merge_requests/636): Removed stray references to deprecated DynamicSparseMatrix class
- [#740](https://gitlab.com/libeigen/eigen/-/merge_requests/740): Removed redundant `nonZeros()` method from `DenseBase` class, which simply called `size()`
- [#752](https://gitlab.com/libeigen/eigen/-/merge_requests/752): Deprecated unused macro EIGEN_GPU_TEST_C99_MATH to reduce code clutter
- [#768](https://gitlab.com/libeigen/eigen/-/merge_requests/768): Removed custom Find*.cmake scripts for BLAS, LAPACK, GLEW, and GSL, now using CMake's built-in modules
- [#793](https://gitlab.com/libeigen/eigen/-/merge_requests/793): Removed unused `EIGEN_HAS_STATIC_ARRAY_TEMPLATE` macro to clean up the codebase
- [#855](https://gitlab.com/libeigen/eigen/-/merge_requests/855): Removed unused macros related to `prsqrt` implementation, improving code clarity and maintainability
- [#897](https://gitlab.com/libeigen/eigen/-/merge_requests/897): Removed obsolete gcc 4.3 copy_bool workaround in testsuite

### Changes

- [#739](https://gitlab.com/libeigen/eigen/-/merge_requests/739): Disabled tests for GCC-4.8 to facilitate transition to C++14

# Unsupported

## Breaking changes

- [#606](https://gitlab.com/libeigen/eigen/-/merge_requests/606): Removal of Sparse Dynamic Matrix from library API
- [#704](https://gitlab.com/libeigen/eigen/-/merge_requests/704): Removed problematic `take<n, numeric_list<T>>` implementation to resolve g++-11 compiler crash

## Major changes

- [#327](https://gitlab.com/libeigen/eigen/-/merge_requests/327): Reimplemented Tensor stream output with new predefined formats and improved IO functionality
- [#534](https://gitlab.com/libeigen/eigen/-/merge_requests/534): Introduces preliminary HIP bfloat16 GPU support for AMD GPUs
- [#577](https://gitlab.com/libeigen/eigen/-/merge_requests/577): Introduces IDR(s)STAB(l) method, a new iterative solver for sparse matrix problems combining features of IDR(s) and BiCGSTAB(l)
- [#612](https://gitlab.com/libeigen/eigen/-/merge_requests/612): Adds support for EIGEN_TENSOR_PLUGIN, EIGEN_TENSORBASE_PLUGIN, and EIGEN_READONLY_TENSORBASE_PLUGIN in tensor classes
- [#622](https://gitlab.com/libeigen/eigen/-/merge_requests/622): Renamed existing Tuple class to Pair and introduced a new Tuple class for improved device compatibility
- [#623](https://gitlab.com/libeigen/eigen/-/merge_requests/623): Introduces device-compatible Tuple implementation for GPU testing, addressing compatibility issues with std::tuple
- [#625](https://gitlab.com/libeigen/eigen/-/merge_requests/625): Introduced new GPU test utilities with flexible kernel execution functions for CPU and GPU environments
- [#676](https://gitlab.com/libeigen/eigen/-/merge_requests/676): Improved accuracy of full tensor reduction for half and bfloat16 types using tree summation algorithm
- [#681](https://gitlab.com/libeigen/eigen/-/merge_requests/681): Prevents integer overflows in EigenMetaKernel indexing for CUDA tensor operations

## Other

### Fixed

- [#653](https://gitlab.com/libeigen/eigen/-/merge_requests/653): Disabled specific HIP subtests that fail due to non-functional device side malloc/free
- [#671](https://gitlab.com/libeigen/eigen/-/merge_requests/671): Fixed GPU special function tests by correcting checks and updating verification methods
- [#679](https://gitlab.com/libeigen/eigen/-/merge_requests/679): Disabled Tree reduction for GPU to resolve memory errors and improve GPU operation stability
- [#695](https://gitlab.com/libeigen/eigen/-/merge_requests/695): Fix compilation compatibility issue with older Boost versions in boostmultiprec test
- [#705](https://gitlab.com/libeigen/eigen/-/merge_requests/705): Fixes TensorReduction test warnings and improves sum accuracy error bound calculation
- [#715](https://gitlab.com/libeigen/eigen/-/merge_requests/715): Fixed failing test for tensor reduction by improving error bound comparisons
- [#723](https://gitlab.com/libeigen/eigen/-/merge_requests/723): Fixed off-by-one error in tensor broadcasting affecting packet size handling
- [#730](https://gitlab.com/libeigen/eigen/-/merge_requests/730): Fixed stride computation for indexed views with non-Eigen index types to prevent potential signed integer overflow
- [#755](https://gitlab.com/libeigen/eigen/-/merge_requests/755): Fixed leftover else branch in unsupported code
- [#770](https://gitlab.com/libeigen/eigen/-/merge_requests/770): Fixed customIndices2Array function to correctly handle the first index in tensor module
- [#853](https://gitlab.com/libeigen/eigen/-/merge_requests/853): Resolved ODR failures in TensorRandom component to improve code stability and reliability
- [#894](https://gitlab.com/libeigen/eigen/-/merge_requests/894): Fixed tensor executor test and added support for tensor packets of size 1
- [#898](https://gitlab.com/libeigen/eigen/-/merge_requests/898): Fixed zeta function edge case for large inputs, preventing NaN and overflow issues
- [#902](https://gitlab.com/libeigen/eigen/-/merge_requests/902): Temporarily disabled aarch64 CI due to unavailable Windows on Arm machines
- [#1001](https://gitlab.com/libeigen/eigen/-/merge_requests/1001): Fixed build compatibility for f16/bf16 Bessel function specializations on AVX512 for older compilers

### Improved

- [#543](https://gitlab.com/libeigen/eigen/-/merge_requests/543): Improved PEP8 compliance and formatting in GDB pretty printer for better code readability
- [#616](https://gitlab.com/libeigen/eigen/-/merge_requests/616): Disabled CUDA Eigen::half host-side vectorization for compatibility with pre-CUDA 10.0 versions
- [#619](https://gitlab.com/libeigen/eigen/-/merge_requests/619): Improved documentation for unsupported sparse iterative solvers
- [#645](https://gitlab.com/libeigen/eigen/-/merge_requests/645): Introduced default constructor for eigen_packet_wrapper to simplify memory operations
- [#669](https://gitlab.com/libeigen/eigen/-/merge_requests/669): Optimized tensor_contract_gpu test by reducing contractions to improve test performance on Windows
- [#678](https://gitlab.com/libeigen/eigen/-/merge_requests/678): Reorganized CUDA/Complex.h to GPU/Complex.h and removed deprecated TensorReductionCuda.h header
- [#724](https://gitlab.com/libeigen/eigen/-/merge_requests/724): Improved TensorIO compatibility with TensorMap containing const elements
- [#896](https://gitlab.com/libeigen/eigen/-/merge_requests/896): Removed ComputeCpp-specific code from SYCL Vptr, improving compatibility and performance
- [#942](https://gitlab.com/libeigen/eigen/-/merge_requests/942): Fixed navbar scroll behavior with table of contents by overriding Doxygen JavaScript
- [#982](https://gitlab.com/libeigen/eigen/-/merge_requests/982): Resolved ambiguities in Tensor comparison operators for C++20 compatibility
- [#1005](https://gitlab.com/libeigen/eigen/-/merge_requests/1005): Re-enabled unit tests for device side malloc in ROCm 5.2

### Added

- [#607](https://gitlab.com/libeigen/eigen/-/merge_requests/607): Added flowchart to help users select sparse iterative solvers in unsupported module
- [#624](https://gitlab.com/libeigen/eigen/-/merge_requests/624): Introduced `Serializer<T>` class for binary serialization, enhancing GPU testing data transfer capabilities
- [#798](https://gitlab.com/libeigen/eigen/-/merge_requests/798): Adds a Non-Negative Least Squares (NNLS) solver to Eigen's unsupported modules using an active-set algorithm
- [#973](https://gitlab.com/libeigen/eigen/-/merge_requests/973): Added `.arg()` method to Tensor class for retrieving indices of max/min values along specified dimensions

### Removed

- [#637](https://gitlab.com/libeigen/eigen/-/merge_requests/637): Removes obsolete DynamicSparseMatrix references and typographical errors in unsupported directory
