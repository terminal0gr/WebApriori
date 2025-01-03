package ca.pfv.spmf.datastructures.collections.set;

import java.util.Arrays;
import java.util.NoSuchElementException;

import ca.pfv.spmf.datastructures.collections.list.ArrayListObject;

/*
 * Copyright (c) 2023 Philippe Fournier-Viger
 *
 * This file is part of the SPMF DATA MINING SOFTWARE
 * (http://www.philippe-fournier-viger.com/spmf).
 *
 * SPMF is free software: you can redistribute it and/or modify it under the
 * terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 *
 * SPMF is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 * A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * SPMF. If not, see <http://www.gnu.org/licenses/>.
 */
/**
 * A hashset to store objects. The hash function is the modulo. The internal
 * structure is an array, and collisions are managed using a custom resizeable
 * array list.
 * 
 * @author Philippe Fournier-Viger
 * @see SetObject
 */
public class AHashSetObject<T> extends SetObject<T>{

	/** Array to store the data */
	private ArrayListObject<T>[] buckets;

	/** Number of elements in the set */
	private int elementCount;

	/** DEFAULT CAPACITY */
	private final int DEFAULT_BUCKET_COUNT = 100;

	/** DEFAULT COLLISION LIST SIZE */
	private int initialCollisionListSize = 10;

	/**
	 * Constructor
	 */
	@SuppressWarnings("unchecked")
	public AHashSetObject() {
		buckets = new ArrayListObject[DEFAULT_BUCKET_COUNT];
		elementCount = 0;
	}

	/**
	 * Constructor
	 * 
	 * @param initialCapacity the initial internal capacity
	 */
	@SuppressWarnings("unchecked")
	public AHashSetObject(int initialCapacity) {
		elementCount = 0;
		buckets = new ArrayListObject[initialCapacity];
	}

	/**
	 * Constructor
	 * 
	 * @param initialCapacity          the initial internal capacity
	 * @param initialCollisionListSize the initial size to be used for each
	 *                                 collision list
	 */
	@SuppressWarnings("unchecked")
	public AHashSetObject(int initialCapacity, int initialCollisionListSize) {
		elementCount = 0;
		buckets = new ArrayListObject[initialCapacity];
		this.initialCollisionListSize = initialCollisionListSize;
	}
	
	/** Constructor using an existing set
	 * @param set a set*/
	public AHashSetObject(SetObject<T> set) {
		this(set.size());
		AEntryIterator x = set.iterator();
		while(x.hasNext()) {
			this.add(x.next());
		}
	}
	
	/** Add all ints from a set
	 * @param set a set*/
	public void addAll(SetObject<T> set) {
		AEntryIterator x = set.iterator();
		while(x.hasNext()) {
			this.add(x.next());
		}
	}
	

	/**
	 * Clear the set
	 */
	public void clear() {
		Arrays.fill(buckets, null);
		elementCount = 0;
	}

	/**
	 * Get the number of elements in the set
	 * 
	 * @return the number
	 */
	public int size() {
		return elementCount;
	}

	/**
	 * Check if this set is empty
	 * 
	 * @return true if empty. Otherwise, false
	 */
	public boolean isEmpty() {
		return elementCount == 0;
	}

	/**
	 * Calculate hash of a key
	 * 
	 * @param key the key
	 * @return the hash value
	 */
	protected int hash(T key) {
		return Math.abs(key.hashCode()) % buckets.length;
	}

	/**
	 * Check if a value is in the structure
	 * 
	 * @param key the key
	 * @return true if it is contained. Otherwise, false
	 */
	public boolean contains(T key) {
		int initialIndex = hash(key);

		if (buckets[initialIndex] == null) {
			return false;
		}

		for (int i = 0; i < buckets[initialIndex].size(); i++) {
			T bucketKey = buckets[initialIndex].get(i);
			if (bucketKey.equals(key)) {
				return true;
			}
		}

		return false;
	}

	/**
	 * Put a new value in the structure
	 * 
	 * @param key the key
	 */
	public void add(T key) {
		int initialIndex = hash(key);

		// If this key is not in the set
		if (buckets[initialIndex] == null) {
			buckets[initialIndex] = new ArrayListObject<T>(initialCollisionListSize);
			buckets[initialIndex].add(key);
			elementCount++;
			return;
		}

		for (int i = 0; i < buckets[initialIndex].size(); i++) {
			T bucketKey = buckets[initialIndex].get(i);
			// If the value is already there
			if (bucketKey.equals(key)) {
				return;
			}
		}

		// otherwise add to the next position
		buckets[initialIndex].add(key);
		elementCount++;
		return;
	}

	/**
	 * Remove a key from the hash table
	 * 
	 * @param key the key
	 * @return true if removed, false if not found
	 */
	public boolean remove(T key) {
		int initialIndex = hash(key);

		// If this key is not in the set
		if (buckets[initialIndex] == null) {
			return false;
		}

		for (int i = 0; i < buckets[initialIndex].size(); i++) {
			T bucketKey = buckets[initialIndex].get(i);
			// If the value is already there
			if (bucketKey.equals(key)) {
				buckets[initialIndex].removeAt(i);
				elementCount--;
				return true;
			}
		}
		return false;
	}

	// ================= ITERATOR
	// =======================================================

	/**
	 * Get an iterator on this map
	 * 
	 * @return an iterator
	 */
	public AEntryIterator iterator() {
		return new AHashSetObjectIterator();
	}

	/**
	 * Iterator for this Set. <br/>
	 * <br/>
	 * Note that the iterator does not check for concurrent modifications and is not
	 * synchronized. It is designed to be used by a single thread, and the map
	 * should not be modified while using the iterator except by calling the
	 * remove() method provided by the iterator. If the map would be modified by
	 * using other methods such as using add() or removeAt(), then the iterator will
	 * not work properly.
	 * 
	 * @author Philippe Fournier-Viger 2023
	 *
	 */
	public class AHashSetObjectIterator extends AEntryIterator {
		/** index of the bucket for the next entry */
		private int bucketIndexNextEntry = 0;
		/** index of the next entry in its bucket */
		private int arrayIndexNextEntry = 0;

		/** index of the bucket for the current entry */
		private int bucketIndexCurrentEntry = -1;
		/** index of the current entry in its bucket */
		private int arrayIndexCurrentEntry = -1;

		/** Next entry */
		private T nextEntry = null;

		/** Next entry */
		private T currentEntry = null;

		/**
		 * Constructor
		 */
		public AHashSetObjectIterator() {

			// If the map is empty, no need to do anything else
			if (elementCount == 0) {
				return;
			}

			// If the map is not empty, we need to find the next element
			for (; bucketIndexNextEntry < buckets.length; bucketIndexNextEntry++) {
				if (buckets[bucketIndexNextEntry] != null && buckets[bucketIndexNextEntry].size() != 0) {
					nextEntry = buckets[bucketIndexNextEntry].get(0);
					return;
				}
			}
		}

		/**
		 * Get the next entry
		 * 
		 * @return the next entry or throws NoSuchElementException if there are no next
		 *         entry
		 */
		public T next() {
			if (nextEntry == null) {
				throw new NoSuchElementException();
			}
			// The next entry becomes the current entry
			currentEntry = nextEntry;
			bucketIndexCurrentEntry = bucketIndexNextEntry;
			arrayIndexCurrentEntry = arrayIndexNextEntry;

			// Then, we need to update the next entry.

			// If there is another entry in the same bucket, this will be the next entry
			if (arrayIndexNextEntry < buckets[bucketIndexNextEntry].size() - 1) {
				arrayIndexNextEntry++;
				nextEntry = buckets[bucketIndexNextEntry].get(arrayIndexNextEntry);
				return currentEntry;
			}

			// Otherwise, look at the next bucket
			arrayIndexNextEntry = 0;
			bucketIndexNextEntry++;
			for (; bucketIndexNextEntry < buckets.length; bucketIndexNextEntry++) {
				if (buckets[bucketIndexNextEntry] != null && buckets[bucketIndexNextEntry].size() != 0) {
					nextEntry = buckets[bucketIndexNextEntry].get(0);
					return currentEntry;
				}
			}

			// We did not find!
			nextEntry = null;

			return currentEntry;
		}

		/**
		 * Check if there is a next entry
		 * 
		 * @return true if there is. Otherwise, false.
		 */
		public boolean hasNext() {
			return nextEntry != null;
		}

		/**
		 * Remove the current entry
		 * 
		 * @return the entry or throw IllegalStateException if there is no current
		 *         entry.
		 */
		public void remove() {
			// If there are no entry, we cannot do this operation
			if (currentEntry == null) {
				throw new IllegalStateException();
			}

			// Remove the current entry
			buckets[bucketIndexCurrentEntry].removeAt(arrayIndexCurrentEntry);

			// If the next entry is in the same bucket, we have
			// to decrease the pointer to the next entry by 1
			// because removing the previous entry will move the elements from the array
			if (bucketIndexCurrentEntry == bucketIndexNextEntry) {
				arrayIndexNextEntry--;
			}

			// Decrease the total number of elements
			elementCount--;
		}
	}
	// =====================================================================
}