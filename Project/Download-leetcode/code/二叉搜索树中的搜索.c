/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     struct TreeNode *left;
 *     struct TreeNode *right;
 * };
 */
//注意结束条件
struct TreeNode* searchBST(struct TreeNode* root, int val) {
    if(!root)
        return NULL;
    if(root->val>val)
        return searchBST(root->left,val);
    else if(root->val<val)
        return searchBST(root->right,val);
    else if(root->val==val)
        return root;
    return NULL;
}