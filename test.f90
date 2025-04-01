module test_module
    implicit none

    ! Real declarations with different kinds
    real(8) :: scalar_real_8 = 1.0d0
    real(4) :: scalar_real_4 = 2.0
    real :: scalar_real_default = 3.0
    real(kind=8) :: scalar_real_kind_8 = 4.0d0
    real(kind=4) :: scalar_real_kind_4 = 5.0
    double precision :: scalar_dp = 5.0d0

    ! Integer declarations
    integer :: scalar_int_default = 4
    integer(8) :: scalar_int_8 = 5

    ! Array declarations
    real(8), dimension(3) :: array_real_8 = [1.0d0, 2.0d0, 3.0d0]
    real(4), dimension(2) :: array_real_4 = [4.0, 5.0]
    integer, dimension(3) :: array_int = [6, 7, 8]
    double precision, dimension(3) :: array_dp = [5.0d0, 4.0d0]

    ! Parameterized variables
    real(8), parameter :: pi = 3.141592653589793d0
    integer, parameter :: max_iter = 100

    ! Pointers and allocatables
    real(8), pointer :: ptr_real => null()
    integer, allocatable :: alloc_array(:)

    ! Custom derived type
    type my_type
        real(8) :: x
        integer :: y
    end type my_type

    ! Variables of custom type
    type(my_type) :: custom_var

contains

    subroutine test_subroutine(a, b, c)
        real(8), intent(in) :: a
        real(4), intent(out) :: b
        integer, intent(inout) :: c

        ! Local variables
        real(8) :: local_real = 1.0d0
        integer :: local_int = 2

        ! Multi-variable declaration
        real(8) :: var1, var2, var3
        real(8) :: initialized_var1 = 3.0d0, initialized_var2 = 4.0d0

        ! Calculations
        b = real(a, kind=4)
        c = c + int(a)
    end subroutine test_subroutine

end module test_module

program main
    use test_module
    implicit none

    ! Main program variables
    real(8) :: main_real = 1.0d0
    integer :: main_int = 2
    real(8), dimension(2) :: main_array = [3.0d0, 4.0d0]

    ! Call subroutine
    call test_subroutine(main_real, main_real, main_int)

    ! Print results
    print *, "main_real =", main_real
    print *, "main_int =", main_int
    print *, "main_array =", main_array
end program main