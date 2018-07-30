set(EXAMPLES_API_PYTHON_DIR ${CMAKE_CURRENT_SOURCE_DIR})

# You cannot have targets with the same name, so we add on Python
set(EXAMPLES_API_PYTHON
    PythonExampleBitVectors
    PythonExampleBitVectorsAndArrays
    PythonExampleCombination
    PythonExampleDatatypes
    PythonExampleFloatingPointArith
    PythonExampleHelloWorld
    PythonExampleLinearArith
    PythonExampleStrings)

foreach(example ${EXAMPLES_API_PYTHON})
  # Strip our prefix
  string(REGEX
         REPLACE "^PythonExample"
                 ""
                 ExampleNoPrefix
                 ${example})
  add_custom_target(${example} DEPENDS _CVC4)
  add_dependencies(examples ${example})
  set(example_test example/api/python/${example})
  add_test(NAME ${example_test}
           COMMAND ${PYTHON_EXECUTABLE}
                   ${EXAMPLES_API_PYTHON_DIR}/${ExampleNoPrefix}.py)
  set_tests_properties(${example_test} PROPERTIES SKIP_RETURN_CODE 77)
  set_tests_properties(${example_test} PROPERTIES LABELS "example")
endforeach()
