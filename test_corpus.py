from corpus import load_corpus, preprocess_corpus, get_unigram_fallback

# 1️⃣ Load corpus
words = load_corpus("data/corpus.txt")
print("✅ Total words loaded:", len(words))
print("🔹 First 10 words:", words[:10])

# 2️⃣ Preprocess
by_len = preprocess_corpus(words)
print("\n✅ Word lengths found:", sorted(by_len.keys())[:10])
print("🔹 Sample 5-letter words:", list(by_len.get(5, []))[:10])

# 3️⃣ Unigram fallback
unigrams = get_unigram_fallback(words)
print("\n✅ Top 10 most frequent letters:", unigrams[:10])
