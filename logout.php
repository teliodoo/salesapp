<?php
        require_once 'classes/init.php';

        $user = new User();
        $user->logout();

        Redirect::to('index.php');
?>