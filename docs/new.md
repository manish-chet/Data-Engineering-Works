??? info "1. Swap consecutive rows in SQL?"
    **Problem:**

    Given a table like this:

    ```
    Input:
    1
    2
    3
    4
    5
    6
    ```

    Desired Output:

    ```
    Output:
    2
    1
    4
    3
    6
    5
    ```

    **Solution using ROW_NUMBER():**

    ```sql
    WITH numbered AS (
        SELECT col, ROW_NUMBER() OVER () AS rn
        FROM your_table
    ),
    swapped AS (
        SELECT
            CASE
                WHEN rn % 2 = 1 THEN rn + 1
                ELSE rn - 1
            END AS new_rn,
            col
        FROM numbered
    )
    SELECT col
    FROM swapped
    ORDER
    ```
    **Using ROW_NUMBER() with CASE + sort trick**
    ```
    WITH numbered AS (
    SELECT val, ROW_NUMBER() OVER (ORDER BY val) AS rn
    ),
    swapped AS (
    SELECT 
        CASE WHEN rn % 2 = 0 THEN rn - 1 ELSE rn + 1 END AS new_rn,
        val
    FROM numbered
    )
    SELECT val
    FROM swapped
    ORDER BY new_rn;
    ```

    **Using ROW_NUMBER() with CASE + sort trick** 
    ```
    WITH numbered AS (
    SELECT val, ROW_NUMBER() OVER (ORDER BY val) AS rn
    )
    SELECT t2.val
    FROM numbered t1
    JOIN numbered t2
    ON CASE
        WHEN t1.rn % 2 = 1 THEN t1.rn + 1 = t2.rn
        ELSE t1.rn - 1 = t2.rn
        END
    ORDER BY t1.rn;
    ```??? info "1. Sort a string according to the frequency of characters"
    Input: str = “geeksforgeeks” 

    Output: forggkksseeee 
    
    Explanation: 
    Frequency of characters: g2 e4 k2 s2 f1 o1 r1 
    Sorted characters according to frequency: f1 o1 r1 g2 k2 s2 e4 
    f, o, r occurs one time so they are ordered lexicographically and so are g, k and s. 
    
    Hence the final output is forggkksseeee
    
    ```
    # Python3 implementation to Sort strings 
    # according to the frequency of 
    # characters in ascending order 

    # Returns count of character in the string 
    def countFrequency(string ,  ch) : 

        count = 0; 

        for i in range(len(string)) :

            # Check for vowel 
            if (string[i] == ch) : 
                count += 1; 

        return count; 

    # Function to sort the string 
    # according to the frequency 
    def sortArr(string) : 
        n = len(string); 

        # Vector to store the frequency of 
        # characters with respective character 
        vp = []; 

        # Inserting frequency 
        # with respective character 
        # in the vector pair 
        for i in range(n) :

            vp.append((countFrequency(string, string[i]), string[i]));
            
        # Sort the vector, this will sort the pair
        # according to the number of characters
        vp.sort();
        
        # Print the sorted vector content
        for i in range(len(vp)) :
            print(vp[i][1],end=""); 

    # Driver code 
    if __name__ == "__main__" :

        string = "geeksforgeeks"; 

        sortArr(string); 

        # This code is contributed by Yash_R
    ```
    **(Optimized Approach - Min Heap Based)**

    ```
        import heapq

    # O(N*LogN) Time, O(Distinct(N)) Space
    def frequencySort(s):
        mpp = {}
        min_heap = []

        for ch in s:
            if ch in mpp:
                mpp[ch] += 1
            else:
                mpp[ch] = 1

        for m in mpp:
            heapq.heappush(min_heap, (mpp[m], m)) # as freq is 1st , char is 2nd

        ans = ""
        #Now we have in the TOP - Less Freq chars
        while min_heap:
            freq, ch = heapq.heappop(min_heap)
            ans += ch * freq # append as many times of freq
        return ans

    # Driver code
    if __name__ == '__main__':
        str = "geeksforgeeks"
        print(frequencySort(str))
     
    # This code is contributed by Prince Kumar
    ```