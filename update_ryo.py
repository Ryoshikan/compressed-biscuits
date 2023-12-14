import os, shutil, sys
from traceback import print_exc
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import configparser
config = configparser.ConfigParser()
current_path = os.path.dirname(os.path.abspath("__file__"))
config_path = os.path.join(current_path, "config.ini")
print("=" * 50)
print("current_path:", current_path)
print("config_path:", config_path)
config.read(config_path)
code_root_path = config.get("Local", "root_path")

# code_root_path = "/root/test/code/"  # 所有脚本的根目录
# 目录结构
# .                             # local_root_path
# ├── config.ini                # 配置文件，位于项目根目录
# ├── encrypt                   # 用来存放加密脚本的文件夹
# │   └── encrypt.py            # 加密脚本
# ├── run.sh                    # 自动化检测更新文件并进行加密的shell脚本
# ├── output.txt                # 保存更新文件列表的文件
# ├── script_code               # 项目文件存放目录
# │   └── compressed-biscuits   # 项目文件
# ├── src                       # 加密后的so文件存放地址
# ├── upload                    # 用于存放上传脚本的文件夹
# │   └── upload2server.py      # 上传脚本
# ├── ssh.rsa                   # git连接github需要用的东西
# └── ssh.rsa.pub               # git连接github需要用的东西


with open(f"{code_root_path}/output.txt", "r") as f:
    res = f.read()
names = res.split("\n")[:-1]
print("Files below waiting for encrypt...")
print("\n".join(names))
print("=" * 50)


def pytoso(name):
    try:
        file_path = f'{code_root_path}script_code/compressed-biscuits/{name}'
        if name.endswith('.py') and os.path.exists(file_path):
            sys.argv = ['encrypt.py', 'build_ext', '--inplace']
            ext_modules = [
                Extension(name.split('.')[0].replace("/", "."), [file_path], extra_compile_args=['-O3']),
            ]

            setup(
                name='Encrypt2so',
                cmdclass={'build_ext': build_ext},
                ext_modules=ext_modules,
                # 共享文件输出文件夹
                package_dir={'': f'{code_root_path}src/'},
            )
    except Exception as e:
        print_exc()
        return 1
    return 0


for name in names:
    try:
        status = pytoso(name)
    except Exception as e:
        print_exc()
    else:
        if status:
            print(f'{name}-加密失败', status)
        else:
            print(f'{name}-加密成功', status)

    finally:
        try:
            os.remove(f'{code_root_path}script_code/compressed-biscuits/{name.replace(".py", ".c")}')
        except Exception as e:
            pass


try:
    shutil.rmtree('build')
except Exception as e:
    pass
