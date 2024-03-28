INSERT INTO Roles (code, name, description, is_active, created_date)
VALUES
 ('ADMIN', 'Administrator', 'User with full permissions', True, '2024-03-06'),
 ('MANAGER', 'Manager', 'User with some administrative permissions', True, '2024-03-06'),
 ('USER', 'Regular User', 'Default role for users', True, '2024-03-06'),
 ('EDITOR', 'Content Editor', 'User with permission to create and edit content', True, '2024-03-06'),
 ('CUSTOMER', 'Customer', 'User with ability to purchase products', True, '2024-03-06');


INSERT INTO Permissions (code, name, description, url_api, method_api, type, is_active, created_date)
VALUES
 ('VIEW_ALL_DATA', 'View All Data', 'Permission to view all data in the system', null, null, 'VIEW', True, '2024-03-06'),
 ('CREATE_PRODUCTS', 'Create Products', 'Permission to create new products', '/api/products', 'POST', 'CREATE', True, '2024-03-06'),
 ('UPDATE_PRODUCTS', 'Update Products', 'Permission to update existing products', '/api/products/{id}', 'PUT', 'UPDATE', True, '2024-03-06'),
 ('DELETE_PRODUCTS', 'Delete Products', 'Permission to delete products', '/api/products/{id}', 'DELETE', 'DELETE', True, '2024-03-06'),
 ('MANAGE_USERS', 'Manage Users', 'Permission to create, update, and delete user accounts', '/api/users', 'any', 'ADMIN', True, '2024-03-06');

INSERT INTO Category (name_category, description, is_active, created_date)
VALUES
 ('Coffee', 'các loại cà phê', True, '2024-03-06'),
 ('Milk tea', 'các loại trà sữa', True, '2024-03-06'),
 ('Soda', 'soda các loại', True, '2024-03-06'),
 ('Cake', 'các loại bánh ngọt', True, '2024-03-06');
