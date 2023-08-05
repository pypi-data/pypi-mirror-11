FILE(REMOVE_RECURSE
  "../modules/packaged_pmem.o"
  "../modules/pmem_pte.ko"
  "libminpmem.pdb"
  "libminpmem.a"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/minpmem.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
