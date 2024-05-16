import React from "react";
import { Container, Row, Col, Button, Card } from "react-bootstrap";
import "./Home.css";

function Home() {
  return (
    <Container fluid>
      <Row className="justify-content-md-center">
        <Col md="auto">
          <h1>WTFunko</h1>
        </Col>
      </Row>
      <Row>
        <Col sm={4}>
          <Card>
            <Card.Img
              variant="top"
              src="https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSs40V37u10PYQCL8nkTSJXNYR6G7kM_rEagLP9Jb5fY9tvveCjiIHCREUvVXSQCOS-P3BzjgWdRsgMFYCnDTasQDin9hdcQ9fpLCWki7Q"
            />
            <Card.Body>
              <Card.Title>Drago Shenron</Card.Title>
              <Card.Text>Realizza i tuoi sogni</Card.Text>
              <Button variant="primary">Acquista ora</Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col sm={4}>
          <Card>
            <Card.Img
              variant="top"
              src="https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcR4RcIMFx-u-mJC8Bao_5eaOmkVqUeZvrrMC6CzcsB2TvjafgQz1zS3I6hAGjAHCBKrrszFUv64SR5guFX-nsi1Z0KBH2NxXI5o6jGcBSBdyqBY85GthBt9Yg"
            />
            <Card.Body>
              <Card.Title>Drago Shenron</Card.Title>
              <Card.Text>Realizza i tuoi sogni</Card.Text>
              <Button variant="primary">Acquista ora</Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col sm={4}>
          <Card>
            <Card.Img
              variant="top"
              src="https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSs40V37u10PYQCL8nkTSJXNYR6G7kM_rEagLP9Jb5fY9tvveCjiIHCREUvVXSQCOS-P3BzjgWdRsgMFYCnDTasQDin9hdcQ9fpLCWki7Q"
            />
            <Card.Body>
              <Card.Title>Drago Shenron</Card.Title>
              <Card.Text>Realizza i tuoi sogni</Card.Text>
              <Button variant="primary">Acquista ora</Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Home;
