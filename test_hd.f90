module test_module
  use HDMod
    implicit none

    ! type(hyperdual) declarations with different kinds
    type(hyperdual) :: scalar_real_8 = hyperdual(1.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual) :: scalar_real_4 = hyperdual(2.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual) :: scalar_real_default = hyperdual(3.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual) :: scalar_real_kind_8 = hyperdual(4.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual) :: scalar_real_kind_4 = hyperdual(5.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual) :: scalar_dp = hyperdual(5.0d0, 0.0d0, 0.0d0, 0.0d0)

    ! type(hyperdual) declarations
    type(hyperdual) :: scalar_int_default = hyperdual(4.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual) :: scalar_int_8 = hyperdual(5.0d0, 0.0d0, 0.0d0, 0.0d0)

    ! Array declarations
    type(hyperdual), dimension(3) :: array_real_8 = [hyperdual(1.0d0, 0.0d0, 0.0d0, 0.0d0), hyperdual(2.0d0, 0.0d0, 0.0d0, 0.0d0), hyperdual(3.0d0, 0.0d0, 0.0d0, 0.0d0)]
    type(hyperdual), dimension(2) :: array_real_4 = [hyperdual(4.0d0, 0.0d0, 0.0d0, 0.0d0), hyperdual(5.0d0, 0.0d0, 0.0d0, 0.0d0)]
    type(hyperdual), dimension(3) :: array_int = [hyperdual(6.0d0, 0.0d0, 0.0d0, 0.0d0), hyperdual(7.0d0, 0.0d0, 0.0d0, 0.0d0), hyperdual(8.0d0, 0.0d0, 0.0d0, 0.0d0)]
    type(hyperdual), dimension(3) :: array_dp = [hyperdual(5.0d0, 0.0d0, 0.0d0, 0.0d0), hyperdual(4.0d0, 0.0d0, 0.0d0, 0.0d0)]

    ! Parameterized variables
    type(hyperdual), parameter :: pi = hyperdual(3.141592653589793d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual), parameter :: max_iter = hyperdual(100.0d0, 0.0d0, 0.0d0, 0.0d0)

    ! Pointers and allocatables
    real(8), pointer :: ptr_real => null()
    type(hyperdual), allocatable :: alloc_array(:)

    ! Custom derived type
    type my_type
        type(hyperdual) :: x
        type(hyperdual) :: y
    end type my_type

    ! Variables of custom type
    type(my_type) :: custom_var

contains

    subroutine test_subroutine(a, b, c)
  use HDMod
        type(hyperdual), intent(in) :: a
        type(hyperdual), intent(out) :: b
        type(hyperdual), intent(inout) :: c

        ! Local variables
        type(hyperdual) :: local_real = hyperdual(1.0d0, 0.0d0, 0.0d0, 0.0d0)
        type(hyperdual) :: local_int = hyperdual(2.0d0, 0.0d0, 0.0d0, 0.0d0)

        ! Multi-variable declaration
        type(hyperdual) :: var1, var2, var3
        type(hyperdual) :: initialized_var1 = hyperdual(3.0d0, 0.0d0, 0.0d0, 0.0d0)
type(hyperdual) :: initialized_var2 = hyperdual(4.0d0, 0.0d0, 0.0d0, 0.0d0)

        ! Calculations
        b = real(a, kind=4)
        c = c + int(a)
    end subroutine test_subroutine

end module test_module

program main
  use HDMod
    use test_module
    implicit none

    ! Main program variables
    type(hyperdual) :: main_real = hyperdual(1.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual) :: main_int = hyperdual(2.0d0, 0.0d0, 0.0d0, 0.0d0)
    type(hyperdual), dimension(2) :: main_array = [hyperdual(3.0d0, 0.0d0, 0.0d0, 0.0d0), hyperdual(4.0d0, 0.0d0, 0.0d0, 0.0d0)]

    ! Call subroutine
    call test_subroutine(main_real, main_real, main_int)

    ! Print results
    print *, "main_real =", main_real
    print *, "main_int =", main_int
    print *, "main_array =", main_array
end program main
