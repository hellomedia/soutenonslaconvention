<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;

class DefaultController extends AbstractController
{
    /**
     * @Route("/", name="index")
     */
    public function index()
    {
        return $this->render('default/index.html.twig');
    }

    /**
     * @Route("/qui-sommes-nous", name="about")
     */
    public function about()
    {
        return $this->render('default/about.html.twig');
    }

    /**
     * @Route("/soutiens", name="soutiens")
     */
    public function soutiens()
    {
        return $this->render('default/soutiens.html.twig');
    }

    /**
     * @Route("/test", name="test")
     */
    public function test()
    {
        return $this->render('default/test.html.twig');
    }
}
