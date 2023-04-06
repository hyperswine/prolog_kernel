from kernel import PrologKernel
from ipykernel.kernelapp import IPKernelApp

IPKernelApp.launch_instance(kernel_class=PrologKernel)
