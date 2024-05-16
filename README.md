# PlagueRAT 

                                                      =-.                              
                                 :-:                   .++-=-                             
                                =:-=*.      :-=++*+=---+=*=-=-                            
                               -::::=+-..-+*++========+++*===**=-.                        
                               -:::--+=+#*+==++++++++====+#*+#*+***=.                     
                               .+---=+**++++++++#%%%%#*+**%%#******+*=                    
                                 -=+=+*++++++++#%*-==#%%+*###***+++*+**:                  
                                   ****++++++++#%+==-*##++#%#***+++**++*-                 
                                  =*+#++++++++++#%###%#*++++***++++***+**:                
                                 .#+***++++**********++++++++=+**++++++++*                
                                 =*++*#*+++*+++++++++++++++++++==+*++++++*:               
                                 +**+++#*++****++++++++++++++++++==+*++++++               
           :-:=====.             *+******#******#******++++++++++++==*++++-               
          +:::--:::::::::::::::-:#*++++*++**************#***+++++++++=+*+*.               
           .::-:-------------====#+++++++++++**************##*#*++++++=+*+                
                                 *+++++++++++++++++++++++++++**##**+++++==                
                                 =+++++++++++++++++++++++++++++++*###+++++                
                                 -++++++++++++++++++++===+==========*%#++++               
                                  #++++++++++++++=====*===========+=*-=*#+*:.             
                                  +++++*++++=========*========-==- .*--::*==-++-          
                                  .+===++=---===+++=++=---*==--.   :-: -===-*--=          
                                   +----*          .+----=.             .. .. ..          
                                -=+:::::+       .:-+-:::-==:                              
                               ===---:-=-+      =-+=-:--+::.                              
                               .:    ::.                                                  
                                                                                        

№ Создайте файл openssl.cnf с таким содержимым:

[ req ]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[ req_distinguished_name ]
CN = {IP.SERVER}  # IP-адрес вашего сервера

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
IP.1 = {IP.SERVER}  # IP-адрес вашего сервера



# Генерация приватного ключа
openssl genpkey -algorithm RSA -out server_key.pem

# Генерация запроса на сертификат с конфигурационным файлом
openssl req -new -key server_key.pem -out server_csr.pem -config openssl.cnf

# Создание самоподписанного сертификата с использованием конфигурационного файла
openssl x509 -req -days 365 -in server_csr.pem -signkey server_key.pem -out server_cert.pem -extensions v3_req -extfile openssl.cnf

# конфигурация
заменить IP в скриптах serve.py и client.py

# ДАННЫЙ СКРИПТ ЯВЛЯЕТЬСЯ УЧЕБНОЙ РАЗРАБОТКОЙ, ИСПОЛЬЗОВАНИЕ ДАННОГО СКРИПТА В НЕПРАВОМЕРНЫХ ЦЕЛЯХ ВАША ОТВЕСТВННОСТЬ