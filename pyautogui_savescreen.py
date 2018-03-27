import time
import pyautogui
# 1328 * 915
# (296,60)
for i in range(151):
    pyautogui.moveTo(1150,270)
    pyautogui.click()
    time.sleep(2)
    pyautogui.screenshot(
        'screenshot/' + str(i * 2 + 1) + '.png',
        region=(295, 50, 1328 / 2, 925))
    pyautogui.screenshot(
        'screenshot/' + str(i * 2 + 2) + '.png',
        region=(295 + 1328 / 2, 50, 1328 / 2, 925))
