import { Layout, Alert, Space, Row, Col, Card, Table, Skeleton, message } from 'antd';
import { Content, Header } from 'antd/es/layout/layout';
import Title from 'antd/es/typography/Title';
import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import axios from "axios";

const http = () => {
  const options = {
    baseURL: `http://127.0.0.1:8080`,
    headers: {
      "Content-Type": "application/json"
    }
  };
  const instance = axios.create(options);
  instance.interceptors.response.use((res) => {
    return res;
  }, (err) => {
    message.error(`呃呃，服务器好像出错了`);
    return Promise.reject(err);
  });
  return instance;
};


const App = () => {
  const [data, setData] = useState(null);
  const columns = [
    {
      title: '组别',
      dataIndex: 'group',
      key: 'group',
      align: 'center'
    },
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      align: 'center'
    },
    {
      title: '角色',
      dataIndex: 'name',
      key: 'name',
      align: 'center'
    },
    {
      title: '票数',
      dataIndex: 'vote',
      key: 'vote',
      align: 'center'
    },
    {
      title: '得票率 (%)',
      dataIndex: 'rate',
      key: 'rate',
      align: 'center'
    },
  ]
  useEffect(() => {
    http().get(`/`).then((res) => setData(res.data)).catch((err) => console.error(err))
  }, [])
  return (
    <Layout>
      <Header style={{ textAlign: "center", backgroundColor: '#fff' }}>
        <Title level={2} style={{ textAlign: "center" }}>
          挺好萌计票（非官方）
        </Title>
      </Header>
      <Content style={{ padding: '20px 50px', backgroundColor: '#fff' }}>
        <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
          <Alert
            message="免责声明"
            description="本计票脚本为自制，与挺好萌官方无关。由于计票脚本的逻辑与官方可能不同，计票结果可能与官方存在差异，敬请知悉。"
            type="info"
            showIcon
          />
          {
            data ?
              <>
                <Row gutter={12} justify='center' style={{ textAlign: "center" }}>
                  <Col xs={12} sm={10} md={8} lg={6}>
                    <Card title="计票时间" style={{ fontSize: 18 }} size='small'>
                      {data.time}
                    </Card>
                  </Col>
                  <Col xs={12} sm={10} md={8} lg={6}>
                    <Card title="投票人数" style={{ fontSize: 18 }} size='small'>
                      {data.voter}
                    </Card>
                  </Col>
                </Row>
                <Table dataSource={data.votes} columns={columns} bordered pagination={false} />
              </>
              : <Skeleton active />
          }
        </Space>
      </Content>
    </Layout>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
