import inspect
import os
import re
import webbrowser
import zipfile

from detect1 import detect as detect1
from detect2 import detect as detect2
from detect3 import detect as detect3
from detect4 import detect as detect4
from detect5 import detect as detect5


if __name__ == "__main__":
    submit_filename = "submit.zip"
    if os.path.exists(submit_filename):
        os.remove(submit_filename)

    funcs_to_submit = [f"detect{i}" for i in range(1, 6)]

    with zipfile.ZipFile(submit_filename, "w") as final_submit_file:
        for func_name in funcs_to_submit:
            func = eval(func_name)

            with final_submit_file.open(f"{func_name}.py", "w") as f:
                func_content = inspect.getsource(func)  # `inspect.getsource` returns the source string of function
                func_content = re.sub(r"\s*show\([\s\S]*?\)", "", func_content)
                func_content = re.sub(r"\s*print\([\s\S]*?\)", "", func_content)
                f.write(func_content.encode("utf-8"))

    print("submit.zip created")

    webbrowser.open("https://aistudio.baidu.com/aistudio/competition/detail/147/0/submit-result")
