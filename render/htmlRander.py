from selenium import webdriver
from selenium.webdriver.edge.options import Options
import os
edge_option=Options()
edge_option.add_argument("--headless")
edge_option.add_argument("--disable-gpu")
edge_option.add_argument("--start-maximized")


def render(fileName:str,fileDir:str, edgedriverpath:str='./render/msedgedriver.exe',edge_option:Options=edge_option) -> str:
    htmlFilePath='file:///'+os.path.abspath(fileDir).replace('\\','/')
    driver=webdriver.Edge(options=edge_option,executable_path=edgedriverpath)
    driver.get(htmlFilePath)
    driver.set_window_size(478,750)

    driver.save_screenshot(f'./pic/{fileName}.png')
    driver.close()
    return 'OK'

if __name__ == "__main__":
    render('test','./htmlpage/test.html')

