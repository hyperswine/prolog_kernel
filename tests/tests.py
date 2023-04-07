import unittest
import jupyter_kernel_test as jkt


class PrologKernelTests(jkt.KernelTests):
    kernel_name = "prolog"
    language_name = "prolog"
    file_extension = ".txt"
    code_x = "hello, world"


if __name__ == "__main__":
    unittest.main()
