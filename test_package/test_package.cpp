#include <libjsonnet++.h>

#include <fstream>
#include <iostream>
#include <streambuf>
#include <string>

bool readFile(const std::string &filename, std::string *output) {
  std::ifstream in(filename);
  if (!in.good()) {

    return false;
  }
  *output = std::string(std::istreambuf_iterator<char>(in),
                        std::istreambuf_iterator<char>());

  return true;
}

int main(int argc, char **argv) {
  std::string input;
  if (!readFile("../../sours.jsonnet", &input)) {
    std::cerr << "Failed to read file" << std::endl;
    return 1;
  }

  jsonnet::Jsonnet jsonnet;
  jsonnet.init();

  std::string output;
  jsonnet.evaluateSnippet("snippet", input, &output);

  if (output.empty()) {
    std::cerr << "Failed to load snippet" << std::endl;
    return 1;
  }

  std::cout << output << std::endl;

  return 0;
}
