def linear_search(parcels, parcel_id):
    for parcel in parcels:
        if parcel.parcel_id == parcel_id:
            return parcel
    return None


def binary_search(parcels, parcel_id):
    left = 0
    right = len(parcels) - 1
    while left <= right:
        middle = (left + right) // 2
        parcel = parcels[middle]
        if parcel.parcel_id == parcel_id:
            return parcel
        if parcel.parcel_id < parcel_id:
            left = middle + 1
        else:
            right = middle - 1
    return None
