#pragma once

// Implementations for generating an x86-64 program that executes in reverse
// order. The source program should be compiled by the script `compile_rev.py`.
//
// Written by MaxXing, 2022-10.
// License GPL-v3.

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <signal.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ucontext.h>

#ifdef REV_TRACE
#include <stdio.h>
#endif

#if !defined(__x86_64__) || !defined(REG_RIP)
#error "x86-64 target required."
#endif

// Start address and end address of the `.text` section.
// Should be provided by the linker script.
extern char rev_text_start, rev_text_end;

// The actual value of variable `rev_text_start` and `rev_text_end`.
#define REV_TEXT_START ((size_t)&rev_text_start)
#define REV_TEXT_END ((size_t)&rev_text_end)

// Bitmap for holding attributes of each byte of the `.text` section.
// One bits in the bitmap corresponds to one byte:
// - 0: Normal byte, or start of instructions that not in "reversed area",
//      no need to do any operation.
// - 1: Start of an instruction.
//
//      7              0
//     +----------------+
//     | byte in bitmap |
//     +----------------+
//      ^              ^
//  byte with      byte with
// larger addr    smaller addr
//
#ifndef REV_BITMAP_SIZE
#define REV_BITMAP_SIZE 256
#endif
static const volatile char rev_text_bytes[REV_BITMAP_SIZE];

// Returns whether the byte at the given address in the `.text` section
// is the start of an instruction.
static inline bool rev_is_inst_start(size_t addr) {
  size_t i = addr - REV_TEXT_START;
  return (rev_text_bytes[i / 8] >> (i % 8)) & 1;
}

// Signal handler for `SIGTRAP`.
static void rev_signal_handler(int signum, siginfo_t *siginfo, void *ptr) {
  // get pointer to the RIP register and read its value
  greg_t *rip = &((ucontext_t *)ptr)->uc_mcontext.gregs[REG_RIP];
  size_t rip_v = (size_t)*rip;

#ifdef REV_TRACE
  // print trace
  fprintf(stderr, "[rev trace] %p", (void *)rip_v);
  if (rip_v >= REV_TEXT_START && rip_v < REV_TEXT_END) {
    fprintf(stderr, " (text+%p)", (void *)(rip_v - REV_TEXT_START));
  }
  fputc('\n', stderr);
#endif

  // do not execute in reverse order if the current instruction
  // is not in the `.text` section
  if (rip_v < REV_TEXT_START || rip_v >= REV_TEXT_END) return;

  // do not execute in reverse order if the current instruction
  // is not in the "reversed area"
  if (!rev_is_inst_start(rip_v)) return;

  // find and jump to the second instruction ahead of the current one
  size_t i, counter = 0;
  for (i = rip_v - 1; counter < 2; --i) counter += rev_is_inst_start(i);
  *rip = (greg_t)i + 1;

#ifdef REV_TRACE
  // print trace
  fprintf(stderr, "[rev trace] back to %p (text+%p)\n", (void *)*rip,
          (void *)(*rip - REV_TEXT_START));
#endif
}

// Toggles the trap flag (TF) in FLAGS register.
static void rev_toggle_tf() {
  asm volatile(
      "pushf\n\t"
      "xorl $0x100, (%rsp)\n\t"
      "popf");
}

// Initializes the trap handler and trap flag.
static void __attribute__((constructor)) rev_initialize() {
  // setup trap handler
  struct sigaction action;
  memset(&action, 0, sizeof(action));
  action.sa_sigaction = rev_signal_handler;
  action.sa_flags = SA_SIGINFO;
  if (sigaction(SIGTRAP, &action, NULL) < 0) abort();
  // enable trap flag
  rev_toggle_tf();
}

// Destructor for clearing the trap flag.
static void __attribute__((destructor)) rev_terminate() {
  // clear trap flag
  rev_toggle_tf();
}
