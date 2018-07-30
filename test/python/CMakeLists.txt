set(python_test_src_files
    BitVectors.py
    BitVectorsAndArrays.py
    Combination.py
    HelloWorld.py
    LinearArith.py)

foreach(src_file ${python_test_src_files})
  string(REPLACE ".py"
                 ""
                 name
                 PythonTest${src_file})
  add_test(NAME ${name}
           COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/${src_file})
  set_tests_properties(${name} PROPERTIES LABELS "python")
endforeach()
