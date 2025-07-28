import os
import matplotlib

matplotlib.use("pygame")

import matplotlib.pyplot as plt

fig = plt.figure()

print(fig.canvas.get_supported_filetypes())

plt.plot([1, 2], [1, 2], color="green")
plt.text(1.5, 1.5, "2", size=50)
plt.xlabel("swag")

plt.savefig("images" + os.sep + "test.jpg")
plt.savefig("images" + os.sep + "test.bmp")
plt.savefig("images" + os.sep + "test2.jpg")
