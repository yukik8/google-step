class Solution():
    def findMajority(self, nums):
        count = 0
        for num in nums:
            if count == 0:
                majority = num
                count += 1
            elif majority == num:
                count += 1
            else:
                count -= 1
        return majority


s = Solution()
print(s.findMajority([1, 4, 5, 5, 5, 10, 5, 10, 2, 5, 5]))
