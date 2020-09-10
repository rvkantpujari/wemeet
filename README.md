<img src="https://raw.githubusercontent.com/rvkantpujari/wemeet/master/wemeet/static/assets/images/logo.png" alt="Bear Stone Smart Home" width="100" height="100" style="display:inline" align="right">

# WeMeet

![GitHub last commit](https://img.shields.io/github/last-commit/rvkantpujari/wemeet?color=red&style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/rvkantpujari/wemeet?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/rvkantpujari/wemeet?color=lightcoral&style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/rvkantpujari/wemeet?color=blueberry&style=for-the-badge)

> #### The project aims to provide a platform for tuition classes, schools, colleges and small organizations where faculties or team leaders can share posts or tasks with students or team members respectively. Faculties or team leaders can also conduct polls.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Functionalities](#functionalities)
- [Snapshots](#snapshots)
<br>

### Prerequisites
What things you need to install

```
You need to install Django v3.0.8 and Pillow
```
<br>

### Installation :man_technologist:
A step by step series of examples that tell you how to get a development env running

- Install with ```pip```
```
  pip install django==3.0.8
   
  pip install pillow
```
<br>

### Functionalities
1. **User**
  - Can register to WeMeet.
  - Can manage profile.
  - Can create or join boards (using code).
  - Accept or reject board invitations.

2. **Board Admin**
  - Can manage board and board members’ permissions and role.
  - Can create posts and polls.
  - Can invite members to board.

3. **Board Member**
  - Can view posts and comment on them.
  - Can participate in polls.
  - Can leave board.
  - Can check the result of polls.

4. **Permissions**
  - All the features of the board are based on permission(s). 
  - If any member has permission(s) only then he or she can perform a particular task.
<br>

### Snapshots

#### Registration page
![01 Register with WeMeet](https://user-images.githubusercontent.com/36390038/92755809-d3ffca00-f3a9-11ea-9d34-dee45e47c3f0.png)

#### Login page
![02 Login with WeMeet](https://user-images.githubusercontent.com/36390038/92756078-188b6580-f3aa-11ea-8c5b-f0eb69626f2f.png)
  
#### Created Boards[Homepage]
![03 Homepage WeMeet](https://user-images.githubusercontent.com/36390038/92756100-1d501980-f3aa-11ea-9c4c-677d59c981e6.png)
  
#### Joined Board
![04 Homepage WeMeet - Join Board](https://user-images.githubusercontent.com/36390038/92756459-78820c00-f3aa-11ea-9a56-105763095a64.png)

#### Invitations to Join Boards
![05 Homepage WeMeet - Invitation](https://user-images.githubusercontent.com/36390038/92756464-79b33900-f3aa-11ea-8cb2-75222411e9b5.png)

#### Create Board
![06 Homepage WeMeet - Create Board](https://user-images.githubusercontent.com/36390038/92756466-7a4bcf80-f3aa-11ea-85dc-8dd051d08885.png)

#### Join Board
![07 Homepage WeMeet - Join Board](https://user-images.githubusercontent.com/36390038/92757005-f34b2700-f3aa-11ea-91d8-6e5c1e23b576.png)

#### Manage Profile
![08 Profile WeMeet](https://user-images.githubusercontent.com/36390038/92757010-f47c5400-f3aa-11ea-886e-5ec790e9ed13.png)

#### Reset Password
![09 Reset Password WeMeet](https://user-images.githubusercontent.com/36390038/92757012-f514ea80-f3aa-11ea-835c-34b9dde66821.png)

#### Board Details
![10 Board Details WeMeet](https://user-images.githubusercontent.com/36390038/92757014-f5ad8100-f3aa-11ea-8cee-28d6eb5f31c8.png)

#### Invite other members using Joining Code
![11 Board Details WeMeet - Joining Code](https://user-images.githubusercontent.com/36390038/92757586-81271200-f3ab-11ea-869b-1c6e0c7abfee.png)

#### Edit Boards Details
![12 Edit Board WeMeet](https://user-images.githubusercontent.com/36390038/92757588-81271200-f3ab-11ea-8be6-5b28d620c7eb.png)

#### Edit Post Details
![14 Edit Post WeMeet](https://user-images.githubusercontent.com/36390038/92757592-82583f00-f3ab-11ea-8c5e-eb91c3f9c3d8.png)

#### Add Comment
![13 Post Details WeMeet - Comment](https://user-images.githubusercontent.com/36390038/92757590-81bfa880-f3ab-11ea-9028-9e75d4f5b54d.png)

#### Edit and Delete Comment
![15 Post Details WeMeet - Edit and Delete Comment](https://user-images.githubusercontent.com/36390038/92758406-4ffb1180-f3ac-11ea-87cd-50678f95ce40.png)

#### Polls
![16 Board Details WeMeet - Polls](https://user-images.githubusercontent.com/36390038/92758538-715bfd80-f3ac-11ea-803f-72260897d30c.png)

#### Invite Member through Email
![17 Board Details WeMeet - Invite Member](https://user-images.githubusercontent.com/36390038/92758547-71f49400-f3ac-11ea-8b7e-256b87e22c41.png)

#### Mute and Remove Member
![18 Board Details WeMeet - Mute and Remove](https://user-images.githubusercontent.com/36390038/92758550-728d2a80-f3ac-11ea-8338-98f82bf6185f.png)

#### Grant Permission
![19 Manage Permissions WeMeet - Grant](https://user-images.githubusercontent.com/36390038/92758713-a49e8c80-f3ac-11ea-85fe-960035565103.png)

#### Revoke Permission
![20 Manage Permissions WeMeet - Revoke](https://user-images.githubusercontent.com/36390038/92758719-a5cfb980-f3ac-11ea-8d58-b3c71c5da9f6.png)
