<?PHP
$wp_dir = "/var/www/html/";
require_once($wp_dir . 'wp-load.php');
function create_posts($name, $file){
    $categoryID = wp_insert_category(array('cat_name' => $name));
    $data = file_get_contents($file);
    $characters = json_decode($data);
    foreach ($characters as $character) {
        $leadTitle = $character->name;
        $leadContent = $character->description;
        $new_post = array(
            'post_title' => $leadTitle,
            'post_content' => $leadContent,
            'post_status' => 'pending',
            'post_author' => 1,
            'post_type' => 'post',
            'post_category' => array($categoryID)
        );
        $post_id = post_exists($leadTitle);
        if ($post_id) {
            echo $post_id . 'already exists<br>';
        }
        else {
            echo 'does not exist<br>';
                $post_id = wp_insert_post($new_post);
                $finaltext = '';
                if ($post_id) {
                    $finaltext .= 'Yay, I made a new post.<br>';
                }
                else {
                    $finaltext .= 'Something went wrong and I didn\'t insert a new post.<br>';
                }
        }
        echo $finaltext;
    }
    }
create_posts("Practice Areas","practice_areas.json");



