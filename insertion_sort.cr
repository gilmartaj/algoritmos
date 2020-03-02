def insertionSort(v : Array)
  i = 1
  while i < v.size
    chave = v[i]
    j = i - 1
    while j >= 0 && v[j] > chave
      v[j + 1] = v[j]
      j = j - 1
    end
    v[j + 1] = chave
    i = i + 1
  end
end
