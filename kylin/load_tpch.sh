sudo git clone https://github.com/electrum/tpch-dbgen.git
cd tpch-dbgen/
sudo apt install make
sudo make
./dbgen -s 1 
sudo docker ps
echo "docker exec -it <container_id> bash"
echo "example: docker exec -it quizzical_payne bash" 

