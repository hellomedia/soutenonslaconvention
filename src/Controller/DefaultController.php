<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Response;

class DefaultController extends AbstractController
{
    /**
     * @Route("/", name="index")
     */
    public function index()
    {
        $response = new Response($this->renderView('default/index.html.twig'), 200);

        $response->headers->set('X-Robots-Tag','index');

        return $response;

        //return $this->render('default/index.html.twig');
    }

    /**
     * @Route("/qui-sommes-nous", name="about")
     */
    public function about()
    {
        $response = new Response($this->renderView('default/about.html.twig'), 200);

        $response->headers->set('X-Robots-Tag','index');

        return $response;

        //return $this->render('default/about.html.twig');
    }

    /**
     * @Route("/soutiens", name="soutiens")
     */
    public function soutiens()
    {
        $response = new Response($this->renderView('default/soutiens.html.twig'), 200);

        $response->headers->set('X-Robots-Tag','index');

        return $response;

        //return $this->render('default/soutiens.html.twig');
    }

    /**
     * @Route("/politique-de-confidentialite", name="privacy")
     */
    public function privacy()
    {
        $response = new Response($this->renderView('default/privacy.html.twig'), 200);

        $response->headers->set('X-Robots-Tag','index');

        return $response;

        //return $this->render('default/privacy.html.twig');
    }
}
