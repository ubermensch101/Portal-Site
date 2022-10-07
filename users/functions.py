import os, subprocess as sp

def check_code(user_file_path, input_file_path,main_output_path, output_file_path):
   with open(f'{input_file_path}', "r") as inp, open(f'{output_file_path}',"w") as out:
      p = sp.Popen(['python3',f'{user_file_path}'], stdin=inp, stdout=out)
   result = sp.run(['diff',f'{main_output_path}',f'{output_file_path}']).returncode
    
   return(result)