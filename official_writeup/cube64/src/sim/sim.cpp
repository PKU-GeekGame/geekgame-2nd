#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <memory>
#include <vector>

#include "VCube64.h"
#include "verilated_fst_c.h"

struct DebugTrace {
  bool write_en;
  int write_sp;
  bool write_data_en;
  int write_data;
  bool swap;
};

std::istream &operator>>(std::istream &is, DebugTrace &dt) {
  char tf;
  int i;
  is >> tf;
  dt.write_en = tf == 't';
  is >> i;
  dt.write_sp = i;
  is >> tf;
  dt.write_data_en = tf == 't';
  is >> i;
  dt.write_data = i;
  is >> tf;
  dt.swap = tf == 't';
  return is;
}

std::ostream &operator<<(std::ostream &os, const DebugTrace &dt) {
  os << "  write_en: " << std::boolalpha << dt.write_en << std::endl;
  os << "  write_sp: " << dt.write_sp << std::endl;
  os << "  write_data_en: " << std::boolalpha << dt.write_data_en << std::endl;
  os << "  write_data: " << dt.write_data << std::endl;
  os << "  swap: " << std::boolalpha << dt.swap << std::endl;
  return os;
}

void panic(const char *message) {
  std::cerr << message << std::endl;
  abort();
}

char b64_int_to_ascii(int i) {
  if (i >= 0 && i <= 25) return 'A' + i;
  if (i >= 26 && i <= 51) return 'a' + i - 26;
  if (i >= 52 && i <= 61) return '0' + i - 52;
  if (i == 62) return '+';
  if (i == 63) return '/';
  panic("invalid base64 character");
}

void tick(std::unique_ptr<VCube64> &top, std::unique_ptr<VerilatedFstC> &tfp,
          std::uint64_t &cycle) {
  top->clock = 0;
  top->eval();
  tfp->dump(cycle * 2);
  top->clock = 1;
  top->eval();
  tfp->dump(cycle * 2 + 1);
  ++cycle;
}

int main(int argc, const char *argv[]) {
  // initialize context and top module
  auto context = std::make_unique<VerilatedContext>();
  context->commandArgs(argc, argv);
  auto top = std::make_unique<VCube64>(context.get());

  // initialize trace
  context->traceEverOn(true);
  auto tfp = std::make_unique<VerilatedFstC>();
  top->trace(tfp.get(), 99);
  tfp->open("trace.fst");
  if (!tfp->isOpen()) panic("failed to open `trace.fst`");

  // open debug trace
  if (argc < 2) panic("expected command line argument TRACE");
  std::ifstream ifs(argv[1]);

  // reset
  std::uint64_t cycle = 0;
  top->reset = 1;
  for (int i = 0; i < 10; ++i) tick(top, tfp, cycle);
  top->reset = 0;

  // run until halt, collect the output
  std::vector<int> output;
  DebugTrace dt;
  bool debug_trace_mismatch = false;
  while (!top->io_halt) {
    tick(top, tfp, cycle);
    if (top->io_hasOutput) {
      output.push_back(top->io_output);
    }

    // check debug trace
    if (top->io_debug_stack_writeEn || top->io_debug_stack_swap) {
      ifs >> dt;
      if (top->io_debug_stack_writeEn != dt.write_en ||
          (dt.write_en && top->io_debug_stack_writeSp != dt.write_sp) ||
          top->io_debug_stack_writeDataEn != dt.write_data_en ||
          (dt.write_data_en &&
           top->io_debug_stack_writeData != dt.write_data) ||
          top->io_debug_stack_swap != dt.swap) {
        debug_trace_mismatch = true;
        break;
      }
    }
  }

  // print the output
  if (debug_trace_mismatch) {
    std::cerr << "debug trace mismatch at cycle " << cycle
              << ", expected:" << std::endl;
    std::cerr << dt;
    return 1;
  } else {
    for (const auto &i : output) std::cout << b64_int_to_ascii(i);
    std::cout << std::endl;
    std::cerr << "finished, " << cycle << " cycle(s) elapsed" << std::endl;
    return 0;
  }
}
