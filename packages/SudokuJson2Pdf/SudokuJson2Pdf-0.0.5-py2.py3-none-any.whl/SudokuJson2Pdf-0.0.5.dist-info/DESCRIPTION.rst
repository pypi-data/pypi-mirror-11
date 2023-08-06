Description: ================
        SudokuJson2Pdf
        ================
        
        This project provides a tool which converts json file of sudoku information to pdf.
        
        How to Install
        ================
        
        ::
        
          $ pip install SudokuJson2pdf
        
        Usage
        =======
        
        ::
        
          $ sudoku2pdf.py [option] question-filename [answer-filename]
        
        For example,
        
        ::
        
          $ cat examples/question1.json
          [
              [
                  [1, 8, 7, 4, 9, 3, 6, 5, 2],
                  [6, 4, 3, 1, 2, 5, 8, 9, 7],
                  [2, 5, 9, 7, 8, 6, 3, 1, 4],
        
                  [7, 1, 4, 2, 3, 8, 5, 6, 9],
                  [9, 6, 8, 5, 7, 1, 4, 2, 3],
                  [5, 3, 2, 6, 4, 9, 1, 7, 8],
        
                  [8, 7, 6, 9, 1, 4, 2, 3, 5],
                  [4, 9, 1, 3, 5, 2, 7, 8, 6],
                  [3, 2, 5, 8, 6, 7, 9, 4, 1]
              ],
              [
                  [8, 4, 6, 9, 2, 7, 5, 1, 3],
                  [3, 5, 2, 8, 4, 1, 9, 7, 6],
                  [7, 1, 9, 6, 3, 5, 4, 2, 8],
        
                  [1, 7, 4, 5, 6, 9, 3, 8, 2],
                  [6, 8, 3, 2, 1, 4, 7, 9, 5],
                  [2, 9, 5, 3, 7, 8, 1, 6, 4],
        
                  [4, 2, 7, 1, 8, 3, 6, 5, 9],
                  [5, 6, 1, 4, 9, 2, 8, 3, 7],
                  [9, 3, 8, 7, 5, 6, 2, 4, 1]
              ]
          ]
        
          $ cat examples/answer1.json
          [
            [
                [1, ".", 7, 4, 9, 3, 6, 5, 2],
                [6, 4, 3, 1, 2, 5, 8, 9, 7],
                [2, 5, 9, 7, 8, 6, 3, 1, 4],
        
                [7, 1, 4, 2, 3, 8, 5, 6, 9],
                [9, 6, 8, 5, 7, 1, 4, 2, 3],
                [5, 3, 2, 6, 4, 9, 1, 7, 8],
        
                [8, 7, 6, 9, 1, 4, 2, 3, 5],
                [4, 9, 1, 3, 5, 2, 7, 8, 6],
                [3, 2, 5, 8, 6, 7, 9, 4, 1]
            ],
            [
                [8, ".", 6, 9, 2, 7, 5, 1, 3],
                [3, 5, 2, 8, 4, 1, 9, 7, 6],
                [7, 1, 9, 6, 3, 5, 4, 2, 8],
        
                [1, 7, 4, 5, 6, 9, 3, 8, 2],
                [6, 8, 3, 2, 1, 4, 7, 9, 5],
                [2, 9, 5, 3, 7, 8, 1, 6, 4],
        
                [4, 2, 7, 1, 8, 3, 6, 5, 9],
                [5, 6, 1, 4, 9, 2, 8, 3, 7],
                [9, 3, 8, 7, 5, 6, 2, 4, "."]
            ]
          ]
        
          $ sudoku2pdf.py examples/question1.json examples/answer1.json -o examples/out.pdf
          $ ls examples/out.pdf
            examples/out.pdf
        
        License
        =========
        
        Apache License 2.0
        
Platform: UNKNOWN
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3
Classifier: Development Status :: 4 - Beta
Classifier: Environment :: Console
Classifier: Topic :: Software Development :: Libraries :: Application Frameworks
Classifier: License :: Freeware
Classifier: License :: OSI Approved :: Apache Software License
Classifier: Intended Audience :: Developers
Classifier: Topic :: Software Development :: Libraries :: Python Modules
