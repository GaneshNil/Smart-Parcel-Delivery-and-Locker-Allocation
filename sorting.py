def partition(parcels, left, right):
    middle = (left + right) // 2
    parcels[middle], parcels[right] = parcels[right], parcels[middle]
    pivot = parcels[right].parcel_id
    boundary = left
    for index in range(left, right):
        if parcels[index].parcel_id < pivot:
            parcels[index], parcels[boundary] = parcels[boundary], parcels[index]
            boundary += 1
    parcels[boundary], parcels[right] = parcels[right], parcels[boundary]
    return boundary


def quick_sort_range(parcels, left, right):
    while left < right:
        pivot = partition(parcels, left, right)
        # Recurse on the smaller side to keep the call stack shallow.
        if pivot - left < right - pivot:
            quick_sort_range(parcels, left, pivot - 1)
            left = pivot + 1
        else:
            quick_sort_range(parcels, pivot + 1, right)
            right = pivot - 1


def quick_sort(parcels):
    result = parcels.copy()
    quick_sort_range(result, 0, len(result) - 1)
    return result


def merge_sort(parcels):
    if len(parcels) <= 1:
        return parcels.copy()

    middle = len(parcels) // 2
    left = merge_sort(parcels[:middle])
    right = merge_sort(parcels[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].destination.casefold() <= right[j].destination.casefold():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
