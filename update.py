"""
File to made updates to the database.

"""
import subprocess

if __name__ == "__main__":
    commands = []
    print("Programa em execucao, digite 0 para sair")
    i = 1
    while i != "0":
        commands = input("Codigos para execucao: ").split("&&")
        for cmd in commands:
            cmd = cmd.strip()
            if cmd:
                res = subprocess.run(cmd, capture_output=True, shell=True, text=True)
                print(f"${cmd}")
                print(res.stdout)
                if res.stderr:
                    print(res.stderr)
        if i == commands and i == 0:
            print("Programa finalizado com sucesso!\nEncerrado o terminal . . .")
            break
