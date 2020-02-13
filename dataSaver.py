import numpy as np

##array[id] => label, start_vcrop, stop_vcrop, n_cols, n_rows, cell_height, cell_width, {0=>img, 1=>nos, 2=>all} ##w.r.t. symbol size
a = [
        [
            ["first", 50, 220, 5, 2, 0.6, 0.6, 2],
            ["last",  220, 400, 5, 2, 0.6, 0.6, 2],
            #["phone", 450, 540, 10, 1, 0.6, 0.6],
            ["photograph", 400, 700, 1, 1, 2, 1.5, 0]
        ],
        [
            ["name", 10, 150, 5,2, 0.6, 0.6, 2],
            ["drug", 200, 350, 5,2, 0.6, 0.6, 2],
            ["dose", 390, 550, 3,1, 0.6, 0.6, 1],
            ["sign", 550, 730, 1,1, 1, 1.5, 0]
        ]
   ]
## dbname, threshold,   folder for pics

np.save("info.npy", b)
np.save("formLogs.npy", a)

#b = np.load("formLogs.npy")
#print(type(b))
#print(b.shape)
