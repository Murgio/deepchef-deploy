import tables
import numpy

hdf5_file_original = tables.open_file('models/vgg16_bottleneck_features_IPCA.hdf5', mode='r')
images_original_1 = hdf5_file_original.root.img_paths
hdf5_path = 'models/image_paths.hdf5'

hdf5_file = tables.open_file(hdf5_path, mode='w')
images = hdf5_file.create_array(hdf5_file.root,
                                               'img_paths', atom=images_original_1.atom,
                                               shape=(images_original_1.nrows,))


images[:images_original_1.nrows] = images_original_1[:]
images.flush()
hdf5_file.close()