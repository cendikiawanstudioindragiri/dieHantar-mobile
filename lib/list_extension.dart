
extension RemoveMiddle<T> on List<T> {
  T removeMiddle() {
    if (isEmpty) {
      throw StateError('Tidak dapat menghapus dari daftar kosong.');
    }
    int middleIndex = (length / 2).floor();
    if (length % 2 == 0) {
      // Untuk daftar genap, ambil elemen tengah yang lebih rendah.
      middleIndex--;
    }
    return removeAt(middleIndex);
  }
}
