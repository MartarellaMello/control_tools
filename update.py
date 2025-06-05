"""
File to made updates to the database.

"""

import subprocess


if __name__ == "__main__":
    print("Selecione uma das opcoes de atualizacao abaixo:\n\n"
          "1 - Atualizar git hub padrao (git push origin main)")
    print("2 - Acessar diretamente o terminal e inserir os comandos manualmente\n"
          "0 - Para sair a qualquer momento do programa. . .\n")
    commands = 7
    print("Programa em execucao, digite 0 para sair")
    while commands != "0":

        commands = input("Codigos para execucao: ").split("&&")

        if commands[0] == "1":
            commands = str("git add .\n"
                           "git commit -m 'Mensagem personalizada'\n"
                           "git push origin main").split("&&")
            txt = str(input("Digite a mensagem de commit: ")).split("&&")
            print(commands)
            commands = str(f"git add .\n"
                           f"git commit -m {txt}\n"
                           f"git push origin main").split("&&")
            for cmd in commands:
                cmd = cmd.strip()
                if cmd:
                    res = subprocess.run(cmd, capture_output=True, shell=True, text=True)
                    print(f"${cmd}")
                    print(res.stdout)
                    if res.stderr:
                        print(res.stderr)
        elif commands[0] == "2":
            commands = str(input("Digite os comandos a serem executados: no git"))
            for cmd in commands:
                cmd = cmd.strip()
                if cmd:
                    res = subprocess.run(cmd, capture_output=True, shell=True, text=True)
                    print(f"${cmd}")
                    print(res.stdout)
                    if res.stderr:
                        print(res.stderr)
        if  commands[0] == "0":
            print("Programa finalizado com sucesso!\nEncerrado o terminal . . .")
            break

