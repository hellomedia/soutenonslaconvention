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
     * @Route("/convention-citoyenne", name="convention-citoyenne")
     */
    public function conventionCitoyenne()
    {
        return $this->render('default/convention-citoyenne.html.twig');
    }

    /**
     * @Route("/qui-sommes-nous", name="about")
     */
    public function about()
    {
        return $this->render('default/about.html.twig');
    }
}
