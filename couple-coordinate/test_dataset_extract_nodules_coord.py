#!/usr/bin/python

import csv, os

out_subset = "nerve-mine-2D/"
# output_path = "/home/ucla/Downloads/tianchi-2D/"
output_path = "/home/jenifferwu/IMAGE_MASKS_DATA/" + out_subset

nodules_coordinate_file = output_path + "image-coordinate/imgs_mask_test_coordinate.csv"

lungs_coordinate_file = output_path + "data_images/test/csv/imgs_mask_test_coordinate.csv"

annotations_file = output_path + "data_images/test/csv/imgs_mask_test_annotations.csv"

csvRows = []


def csv_row(seriesuid, coordX, coordY, coordZ, diameter_mm):
    new_row = []
    new_row.append(seriesuid)
    new_row.append(coordX)
    new_row.append(coordY)
    new_row.append(coordZ)
    new_row.append(diameter_mm)
    csvRows.append(new_row)


def get_lungs_nodules(nodules_csvRows, lungs_csvRows):
    for nodule_row in nodules_csvRows:
        seriesuid = nodule_row['seriesuid']
        nodule_coordZ, nodule_coordX, nodule_diameter_mm = nodule_row["coordX"], nodule_row["coordY"], nodule_row["diameter_mm"]
        # nodule_coordX, nodule_coordY, nodule_diameter_mm = "-88.20063783", "63.04192832", "7.734742324"
        # print(nodule_coordX, nodule_coordZ, nodule_diameter_mm)
        for lung_row in lungs_csvRows:
            lung_coordX, lung_coordY, lung_coordZ = lung_row["coordX"], lung_row["coordY"], lung_row["coordZ"]
            # print(lung_coordX, lung_coordY, lung_coordZ)
            # print(nodule_coordX, lung_coordX, abs(float(nodule_coordX) - float(lung_coordX)))
            # print(nodule_coordY, lung_coordY, abs(float(nodule_coordY) - float(lung_coordY)))
            if abs(abs(float(nodule_coordX)) - float(lung_coordX)) <= 10 and abs(abs(float(nodule_coordZ)) - float(lung_coordZ)) <= 10:
                csv_row(seriesuid, nodule_coordX, lung_coordY, nodule_coordZ, nodule_diameter_mm)


if __name__ == '__main__':
    seriesuid = "1.3.6.1.4.1.14519.5.2.1.6279.6001.367204840301639918160517361062"

    # Read the CSV file in (skipping first row).
    nodules_csvRows = []
    csvFileObj = open(nodules_coordinate_file)
    readerObj = csv.DictReader(csvFileObj)
    for row in readerObj:
        if row['seriesuid'].replace(".mhd", "") == seriesuid:
            # print(row)
            nodules_csvRows.append(row)

    lungs_csvRows = []
    csvFileObj = open(lungs_coordinate_file)
    readerObj = csv.DictReader(csvFileObj)
    for row in readerObj:
        if row['seriesuid'] == seriesuid:
            # print(row)
            lungs_csvRows.append(row)

    get_lungs_nodules(nodules_csvRows, lungs_csvRows)

    # Write out the imgs_mask_test_annotations CSV file.
    print(os.path.join(output_path, annotations_file))
    csvFileObj = open(os.path.join(output_path, annotations_file), 'w')
    csvWriter = csv.writer(csvFileObj)
    for row in csvRows:
        # print row
        csvWriter.writerow(row)
    csvFileObj.close()
