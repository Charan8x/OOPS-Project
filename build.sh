# Create build.sh file with this content:
#!/bin/bash
pip install -r requirements.txt
mkdir -p cpp_core/include/nlohmann
wget -O cpp_core/include/nlohmann/json.hpp https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp
cd cpp_core
g++ -o main main.cpp -I./include -std=c++17
chmod +x main
cd ..

# Then:
chmod +x build.sh
git add build.sh
git commit -m "Add build script"
git push